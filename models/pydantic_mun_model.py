from pydantic import BaseModel


from datetime import datetime
from typing import Optional


class Tag(BaseModel):
    title: Optional[str] = None
    slug: Optional[str] = None
    path: Optional[str] = None


class Image(BaseModel):
    author: Optional[str] = None
    source: Optional[str] = None
    description: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    image_90: Optional[str] = None
    image_250: Optional[str] = None
    image_800: Optional[str] = None
    image_1600: Optional[str] = None


class ContentBase(BaseModel):
    position: Optional[int] = None
    kind: Optional[str] = None
    text: Optional[str] = None


class Content(ContentBase):
    images: Optional[list[Image]] = None


class ArticleBase(BaseModel):
    title: str
    published_at: datetime
    lead: str
    rubric_title: Optional[str] = None
    type: Optional[str] = None
    authors: list[str] | str | None = None


class Article(ArticleBase):
    tags: Optional[list[Tag]] = None
    content_blocks: Optional[list[Content]] = None
    image: Optional[Image] = None
    site_link: Optional[str] = None


class News(BaseModel):
    title: str
    path: str
    published_at: datetime
    images_count: int
    lead: str
    article: Optional[Article] = None
    image: Optional[Image] = None
