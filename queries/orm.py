import logging


from sqlalchemy import select
# from sqlalchemy.orm import joinedload, selectinload


from database import Base, engine, session_fabric
from models.sqlalchemy_model import (
    # NewsOrm,
    ContentOrm,
    ArticleOrm,
    ImageOrm,
    # TagOrm,
    # ArticleTag,
    SourceOrm
)
from models.pydantic_mun_model import (
    Article,
    ContentBase,
    Image
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
            source_list = [SourceOrm(**source) for source in sources]
            session.add_all(source_list)
            session.commit()

    @staticmethod
    def insert_news_to_db(article_clear: dict[any, any], article: Article):
        with session_fabric() as session:
            source_id = SyncOrm.get_source_id_by_url(
                article.site_link,
                session
                )

            img_id = None
            if article.image:
                img_id = SyncOrm.create_image_record(
                    list(article.image.model_dump()),
                    session
                    )

            article_dict = {
                **article_clear,
                'source_id': source_id,
                'image_id': img_id}

            artical_orm = ArticleOrm(**article_dict)
            session.add(artical_orm)
            session.flush()
            print(artical_orm.id)
            # for content in article.content_blocks:
            #     content_base = ContentBase(**content.model_dump())
            #     content_orm = content_base
            #     content_orm
            #     if content.images:
            # session.commit()

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
        for image in images:
            image_orm = {**image, 'content_id': content_id}
            session.add(
                ImageOrm(**image_orm)
                )
        if not content_id:
            return image_orm.id
        return None
