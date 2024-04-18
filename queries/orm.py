from sqlalchemy.orm import joinedload, selectinload


from database import Base, engine, session_fabric
from models.sqlalchemy_model import (
    # NewsOrm,
    ContentOrm,
    ArticleOrm,
    ImageOrm,
    TagOrm,
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
            session.commit()

    @staticmethod
    def _is_pydantic(obj: object):
        """Checks whether an object is pydantic."""
        return type(obj).__class__.__name__ == "ModelMetaclass"

    @staticmethod
    def parse_pydantic_schema(schema):
        parsed_schema = dict(schema)
        for key, value in parsed_schema.items():
            try:
                if isinstance(value, list) and len(value):
                    if SyncOrm.is_pydantic(value[0]):
                        parsed_schema[key] = [schema.Meta.orm_model(**schema.dict()) for schema in value]
                else:
                    if SyncOrm.is_pydantic(value):
                        parsed_schema[key] = value.Meta.orm_model(**value.dict())
            except AttributeError:
                raise AttributeError("Found nested Pydantic model but Meta.orm_model was not specified.")
        return parsed_schema
