# from sqlalchemy.orm import joinedload, selectinload


from database import Base, engine, session_fabric
from models.sqlalchemy_model import (
    # NewsOrm,
    ContentOrm,
    ArticleOrm,
    # ImageOrm,
    # TagOrm,
    # ArticleTag,
    SourceOrm
)
from models.pydantic_mun_model import (
    Article,
    ContentBase,
    Image
)


class SyncOrm:
    @staticmethod
    def create_table():
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)

    @staticmethod
    def fill_catalog(sources):
        with session_fabric() as session:
            source_list = [SourceOrm(**source) for source in sources]
            session.add_all(source_list)
            session.commit()

    @staticmethod
    def insert_news_to_db(article_clear: dict[any, any], article: Article):
        with session_fabric() as session:
            artical_orm = ArticleOrm(**article_clear)
            session.add(artical_orm)
            session.flush()
            # for content in article.content_blocks:
            #     content_base = ContentBase(**content.model_dump())
            #     content_orm = content_base
            #     content_orm
            #     if content.images:
            session.commit()
