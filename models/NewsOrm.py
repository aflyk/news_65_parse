from database import Base


from sqlalchemy.orm import Mapped


from datetime import datetime
from typing import Optional


class NewsOrm(Base):
    __tablename__ = 'news'

    title: Mapped[str]
    path: Mapped[str]
    published_at: Mapped[datetime]
    images_count: Mapped[int]
    lead: Mapped[str]
    source: Mapped[Optional[str]]
