import hashlib
import logging


from sqlalchemy import select, inspect
from sqlalchemy.orm import Session


from database import Base, engine, session_fabric
from models.sqlalchemy_model import (
    ContentOrm,
    ArticleOrm,
    ImageOrm,
    TagOrm,
    SourceOrm,
    RubricOrm,
    ThemeOrm,
)
from models.pydantic_mun_model import (
    Article,
    ArticleBase,
    ContentBase,
    Image
)
from config import settings


log = logging.getLogger(__name__)


class SyncOrm:
    @staticmethod
    def get_source_id_by_url(url: str, session) -> int:
        source_orm = session.query(SourceOrm).filter_by(url=url)
        source = source_orm.one()
        return source.id

    @staticmethod
    def create_table(sources):
        if not inspect(engine).has_table('source',
                                         schema=settings.POSTGRES_SCHEMA):
            Base.metadata.drop_all(bind=engine)
            log.debug('Таблицы удалены')
            Base.metadata.create_all(bind=engine)
            log.debug('Новые таблицы созданы')
            SyncOrm.fill_catalog(sources)

    @staticmethod
    def fill_catalog(sources):
        with session_fabric() as session:
            log.debug('Заполнение таблицы source')
            source_list = [SourceOrm(**source) for source in sources]
            session.add_all(source_list)
            theme_list = [ThemeOrm(title=theme)
                          for theme in settings.theme_dict]
            session.add_all(theme_list)
            session.commit()
            log.debug('Справочники заполнены')

    @staticmethod
    def get_article_image(article: Article) -> ImageOrm | None:
        log.info('Получаем к статье фото')
        if article.image:
            try:
                picture = ImageOrm(**article.image.model_dump())
            except Exception as e:
                log.exception('Не получилось данные привести к модели '
                              f'ImageOrm\n{article.image}\n'
                              f'Ошибка {e}')
            log.info('Фото к статье получено')
            return picture
        log.info(f'Фото к статье не найдено {article.title}'
                 f'с сайта {article.site_link}')
        return None

    @staticmethod
    def get_article_rubric(article: Article, session) -> RubricOrm | None:
        log.info('Получаем рубрику')
        rubric_title = article.rubric_title
        if rubric_title:
            query = (
                select(RubricOrm)
                .filter_by(title=rubric_title.title)
            )
            rubric_orm = SyncOrm.get_one_or_none(query, session)

            if not rubric_orm:
                try:
                    rubric_orm = RubricOrm(**rubric_title.model_dump())
                    theme_orm = SyncOrm.get_theme(rubric_title.title, session)
                    rubric_orm.theme_id = theme_orm.id
                except Exception as e:
                    log.exception('Не получилось данные привести к модели '
                                  f'RubricOrm\n{rubric_title}\n'
                                  f'Ошибка {e}')
            log.info('Рубрика получена')
            return rubric_orm
        log.info(f'Рубрика к статье не найдена {article.title}'
                 f'с сайта {article.site_link}')
        return None

    @staticmethod
    def get_theme(rubric_title: str, session: Session) -> ThemeOrm | None:
        log.info('Получаем тематику')
        for key, val in settings.theme_dict.items():
            if rubric_title.lower() in val:
                query = (
                    select(ThemeOrm)
                    .filter_by(title=key)
                )
                break
        else:
            query = (
                select(ThemeOrm)
                .filter_by(title='не распределенно')
            )
        theme_orm = SyncOrm.get_one_or_none(query, session)
        log.info('Тематика получена')
        return theme_orm

    @staticmethod
    def get_content_image(
            images: list[Image] | None = None
            ) -> list[ImageOrm] | None:
        log.info('Получаем контент фото')
        if images:
            img_list = []
            for img in images:
                try:
                    img_list.append(ImageOrm(**img.model_dump()))
                except Exception as e:
                    log.exception('Не получилось данные привести к модели '
                                  f'ImageOrm\n{img}\n'
                                  f'Ошибка {e}')
            return img_list
        return None

    @staticmethod
    def get_article_content_block(article: Article) -> list[ContentOrm] | None:
        log.info('Получаем контент блоки')
        content_blocks = []
        for content in article.content_blocks:
            try:
                content_for_orm = ContentBase(**content.model_dump())
                content_orm = ContentOrm(**content_for_orm.model_dump())
            except Exception as e:
                log.exception(f'Произошла ошибка добавления контента {e}\n'
                              f'{content.model_dump()}')
            content_image = SyncOrm.get_content_image(content.images)
            if content_image:
                content_orm.images = content_image
            content_blocks.append(content_orm)
        log.info('Контент блоки полученны')
        return content_blocks

    @staticmethod
    def get_one_or_none(query, session):
        return session.execute(query).scalars().one_or_none()

    @staticmethod
    def get_article_tags(article: Article, session) -> list[TagOrm] | list:
        log.info('Получаем тэги')
        tags_list = []
        for tag in article.tags:
            tag_title = tag.title
            query = (
                select(TagOrm)
                .filter_by(title=tag_title)
            )
            log.debug(f'Обрабатывается тег {tag_title}')
            tag_orm = SyncOrm.get_one_or_none(query, session)
            log.debug(f'Полученны данные {tag_orm}')
            if not tag_orm:
                log.info(f'Добавляем тэг {tag} в бд')
                try:
                    tag_orm = TagOrm(**tag.model_dump())
                except Exception as e:
                    log.exception('Не получилось данные привести к модели '
                                  f'TagOrm\n{tag}\n'
                                  f'Ошибка {e}')
                log.info(f'Тэг {tag} добавлен')
            if not any(map(lambda x: x.title == tag_orm.title, tags_list)):
                tags_list.append(tag_orm)
        return tags_list

    @staticmethod
    def check_article(
                article: Article,
                hash_value: str,
                source_id: int,
                session: Session,
                ) -> None:
        query = (
            select(ArticleOrm)
            .filter_by(
                source_id=source_id,
                title=article.title
                )
            )
        article_orm = SyncOrm.get_one_or_none(query, session)

        if article_orm and (article_orm.hash != hash_value):
            # организовать удаление записи или апдейт?
            log.info(f'Update is not equal {article_orm.hash}!={hash_value} ')
            article_clear = ArticleBase(**article.model_dump()).model_dump()
            article_dict = {
                **article_clear,
                'source_id': source_id,
                'hash': hash_value,
                }
            article_orm = ArticleOrm(**article_dict)
            article_orm = SyncOrm.update_article(
                article_orm,
                article,
                session
                )
            return True
        elif article_orm and (article_orm.hash == hash_value):
            log.info('Обновлений не требуется')
            return True
        return False

    @staticmethod
    def update_article(
            article_orm: ArticleOrm,
            article: Article,
            session: Session
            ) -> ArticleOrm:
        log.info('Обновление вложений')
        log.info(f'Было {article_orm}')
        article_orm.image = SyncOrm.get_article_image(article)
        article_orm.content_blocks = (
            SyncOrm.get_article_content_block(article)
            )
        article_orm.tags = SyncOrm.get_article_tags(article, session)
        log.info(f'Стало {article_orm}')
        log.info('Вложения обновлены')
        return article_orm

    @staticmethod
    def get_hash(article: Article):
        hash_object = hashlib.sha256(article.model_dump_json().encode())
        hash_value = hash_object.hexdigest()
        return hash_value

    @staticmethod
    def pre_write_check(article: Article, session: Session):
        # получение id ресурса с которого тянется новость
        source_id = SyncOrm.get_source_id_by_url(
            article.site_link,
            session
            )
        # вычисление хэша с новости
        hash_value = SyncOrm.get_hash(article)
        # проверка на существования статьи
        check = SyncOrm.check_article(article, hash_value, source_id, session)

        return (source_id, hash_value, check)

    @staticmethod
    def insert_news_to_db(article_clear: dict[any, any], article: Article):
        with session_fabric() as session:
            source_id, hash_value, check = SyncOrm.pre_write_check(
                article,
                session,
                )

            if check:
                session.commit()
                return None

            log.debug(f'Получение новости с сайта {article.site_link}')
            article_dict = {
                **article_clear,
                'source_id': source_id,
                'hash': hash_value,
                }

            log.info('Попытка преобразовать данные article_dict к sql модели')
            try:
                article_orm = ArticleOrm(**article_dict)
            except Exception as e:
                log.exception('Не получилось данные привести к модели '
                              f'ArticleOrm\n{article_dict}\n'
                              f'Ошибка {e}')
            log.info('Получена модель ArticleOrm')

            try:
                article_orm.image = SyncOrm.get_article_image(article)

                article_orm.content_blocks = (
                    SyncOrm.get_article_content_block(article)
                    )

                rubric = SyncOrm.get_article_rubric(article, session)
                if rubric is None:
                    article_orm.rubric = None
                elif rubric.id:
                    article_orm.rubric_id = rubric.id
                    article_orm.theme_id = rubric.theme_id
                else:
                    article_orm.rubric = rubric
                    article_orm.theme_id = rubric.theme_id

                # theme = SyncOrm.get_theme(article.rubric_title.title, session)
                # if theme:
                #     article_orm.theme = theme

                article_orm.tags = SyncOrm.get_article_tags(article, session)

            except Exception as e:
                log.exception(f'{e}\n {article}')
                raise

            session.add(article_orm)
            session.commit()
