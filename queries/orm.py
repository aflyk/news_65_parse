import logging


# from sqlalchemy import select
# from sqlalchemy.orm import joinedload, selectinload


from database import Base, engine, session_fabric
from models.sqlalchemy_model import (
    ContentOrm,
    ArticleOrm,
    ImageOrm,
    TagOrm,
    SourceOrm
)
from models.pydantic_mun_model import (
    Article
)


log = logging.getLogger(__name__)


class SyncOrm:
    @staticmethod
    def create_table():
        Base.metadata.drop_all(bind=engine)
        log.debug('Таблицы удалены')
        Base.metadata.create_all(bind=engine)
        log.debug('Новые таблицы созданы')

    @staticmethod
    def fill_catalog(sources):
        with session_fabric() as session:
            log.debug('Заполнение таблицы source')
            source_list = [SourceOrm(**source) for source in sources]
            session.add_all(source_list)
            session.commit()
            log.debug('Справочники заполнены')

    @staticmethod
    def insert_news_to_db(article_clear: dict[any, any], article: Article):
        with session_fabric() as session:
            source_id = SyncOrm.get_source_id_by_url(
                article.site_link,
                session
                )
            log.debug(f'Получение новости с сайта {article.site_link}')
            article_dict = {
                **article_clear,
                'source_id': source_id}
            log.debug('Запись основной информации о статье')
            artical_orm = ArticleOrm(**article_dict)
            log.debug('Сохраяняем фото к статье')
            artical_orm.image = ImageOrm(**article.image.model_dump())
            log.debug('Начинаем работу с блоком контента')
            content_blocks = []
            for content in article.content_blocks:
                content_orm = ContentOrm(**content.model_dump())
                if content.images:
                    img_list = []
                    for img in content.images:
                        img_list.append(ImageOrm(**img.model_dump()))
                    content_orm.images = img_list
                content_blocks.append(content_orm)
            log.debug('Сохраняем блок контента')
            artical_orm.content_blocks = content_blocks
            tags_list = [TagOrm(**tag.model_dump()) for tag in article.tags]
            artical_orm.tags = tags_list
            session.add(artical_orm)
            session.flush()

            session.commit()

    @staticmethod
    def get_source_id_by_url(url: str, session) -> int:
        source_orm = session.query(SourceOrm).filter_by(url=url)
        source = source_orm.one()
        return source.id

    @staticmethod
    def create_image_record(images: list[dict[str, str]],
                            session,
                            content_id: int | None = None
                            ) -> int | None:
        try:
            for image in images:
                image_orm = {**image, 'content_id': content_id}
                session.add(
                    ImageOrm(**image_orm)
                    )
            if not content_id:
                return image_orm.id
            return None
        except Exception as e:
            log.debug(f'Возникла проблема {e} с добавлением \n{image}\n'
                      'в таблицу image')
