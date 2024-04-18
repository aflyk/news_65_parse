from datetime import datetime
from sqlalchemy import create_engine, MetaData, text
from sqlalchemy.orm import (
    sessionmaker,
    DeclarativeBase,
    Mapped,
    mapped_column)
from config import settings


engine = create_engine(
    url=settings.DATABASE_URL_psycopg,
    echo=True,
)

session_fabric = sessionmaker(engine)


class Base(DeclarativeBase):
    metadata = MetaData(schema='public')

    id: Mapped[int] = mapped_column(primary_key=True)

    сreated_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.now,
    )

    repr_cols_num = 3
    repr_cols = tuple()

    def __repr__(self):
        """Relationship не используется в repr(), т.к. могут
        вести к неожиданным подгрузкам"""
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f'{col}={getattr(self, col)}')

        return f'<{self.__class__.__name__} {", ".join(cols)}>'
