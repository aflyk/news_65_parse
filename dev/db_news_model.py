from datetime import datetime
from typing import Optional


from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


from database import Base


# class NewsOrm(Base):
#     __tablename__ = 'news'

#     title: Mapped[str]
#     path: Mapped[str]
#     published_at: Mapped[datetime]
#     images_count: Mapped[int]
#     lead: Mapped[str]
#     source: Mapped[Optional[str]]

#     article: Mapped['ArticleOrm'] = relationship(
#         back_populates='news',
#     )


class ArticleOrm(Base):
    __tablename__ = 'article'

    title: Mapped[str]
    published_at: Mapped[datetime]
    lead: Mapped[str]
    rubric_title: Mapped[str]
    type: Mapped[str]
    authors: Mapped[str]
    site_link: Mapped[str]
    # news_id: Mapped[int] = mapped_column(
    #     ForeignKey('news.id', ondelete='CASCADE', name="fk_article_news")
    # )

    # news: Mapped['NewsOrm'] = relationship(
    #     back_populates='article',
    # )
    content_blocks: Mapped['ContentOrm'] = relationship(
        back_populates='article'
    )
    tags: Mapped['TagOrm'] = relationship(
        back_populates='article',
        secondary='article_tag'
    )


class ContentOrm(Base):
    __tablename__ = 'content'

    position: Mapped[Optional[int]]
    kind: Mapped[Optional[str]]
    text: Mapped[Optional[str]]
    images_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey('image.id', ondelete='CASCADE', name='fk_content_image')
    )
    article_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey('article.id', ondelete='CASCADE', name='fk_article_content')
    )

    article: Mapped['ArticleOrm'] = relationship(
        back_populates='content_blocks'
    )


class ImageOrm(Base):
    __tablename__ = 'image'

    author: Mapped[Optional[str]]
    source: Mapped[Optional[str]]
    description: Mapped[Optional[str]]
    width: Mapped[Optional[int]]
    height: Mapped[Optional[int]]
    image_90: Mapped[Optional[str]]
    image_250: Mapped[Optional[str]]
    image_800: Mapped[Optional[str]]
    image_1600: Mapped[Optional[str]]

    # news_id: Mapped[int] = mapped_column(
    #     ForeignKey('news.id', name='fk_image_news')
    # )
    article_id: Mapped[int] = mapped_column(
        ForeignKey('article.id', name='fk_article_image')
    )
    content_id: Mapped[int] = mapped_column(
        ForeignKey('content.id', name='fk_content_image')
    )


class TagOrm(Base):
    __tablename__ = 'tag'

    title: Mapped[Optional[str]]
    slug: Mapped[Optional[str]]
    path: Mapped[Optional[str]]

    article: Mapped['ArticleOrm'] = relationship(
        back_populates='tags',
        secondary='article_tag'
    )


class ArticleTag(Base):
    __tablename__ = 'article_tag'

    article_id: Mapped[int] = mapped_column(
        ForeignKey('article.id', name='fk_article_articletag'),
        primary_key=True
    )
    tag_id: Mapped[int] = mapped_column(
        ForeignKey('tag.id', name='fk_articletag_tag'),
        primary_key=True
    )
