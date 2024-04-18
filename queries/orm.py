# from sqlalchemy.orm import joinedload, selectinload


from database import Base, engine, session_fabric
from models.sqlalchemy_model import (
    # NewsOrm,
    ContentOrm,
    ArticleOrm,
    # ImageOrm,
    # TagOrm,
    # ArticleTag
)
from models.pydantic_mun_model import Article


class SyncOrm:
    @staticmethod
    def create_table():
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)

    @staticmethod
    def insert_news_to_db(article_clear: dict[any, any], article: Article):
        with session_fabric() as session:
            artical_orm = ArticleOrm(**article_clear)
            session.add(artical_orm)
            session.flush()
            for content in article.content_blocks:
                content_orm = ContentOrm(**content.model_dump())
                content_orm
            session.commit()
