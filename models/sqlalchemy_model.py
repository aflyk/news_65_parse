"""
Статья о том как поженить pydantic с sqlachemy
https://stackoverflow.com/questions/64414030/how-to-use-nested-pydantic-models-for-sqlalchemy-in-a-flexible-way
"""
from datetime import datetime
from typing import Optional


from sqlalchemy import ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship


from database import Base


article_tag = Table(
    'article_tag',
    Base.metadata,
    Column('article_id', ForeignKey('article.id'), primary_key=True),
    Column('tag_id', ForeignKey('tag.id'), primary_key=True)
)

# class ArticleTag(Base):
#     __tablename__ = 'article_tag'

#     article_id: Mapped[int] = mapped_column(
#         ForeignKey('article.id', name='fk_article_articletag'),
#         primary_key=True
#     )
#     tag_id: Mapped[int] = mapped_column(
#         ForeignKey('tag.id', name='fk_articletag_tag'),
#         primary_key=True
#     )


class ArticleOrm(Base):
    __tablename__ = 'article'

    title: Mapped[str]
    published_at: Mapped[datetime]
    lead: Mapped[str]
    rubric_title: Mapped[str]
    type: Mapped[str]
    hash: Mapped[str]
    authors: Mapped[Optional[str]]

    source_id: Mapped[int] = mapped_column(
        ForeignKey('source.id', name='fk_article_source')
    )
    image_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey('image.id', name='fk_article_image')
    )

    content_blocks: Mapped[list['ContentOrm']] = relationship(
        back_populates='article'
    )
    image: Mapped['ImageOrm'] = relationship(
        back_populates='article'
    )
    source: Mapped['SourceOrm'] = relationship(
        back_populates='article'
    )
    tags: Mapped[list['TagOrm']] = relationship(
        back_populates='article',
        secondary=article_tag
    )


class ContentOrm(Base):
    __tablename__ = 'content'

    position: Mapped[Optional[int]]
    kind: Mapped[Optional[str]]
    text: Mapped[Optional[str]]
    article_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey('article.id', ondelete='CASCADE', name='fk_article_content')
    )

    article: Mapped['ArticleOrm'] = relationship(
        back_populates='content_blocks'
    )
    images: Mapped[list['ImageOrm']] = relationship(
        back_populates='content'
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

    content_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey('content.id', name='fk_content_image'),
    )

    article: Mapped['ArticleOrm'] = relationship(
        back_populates='image',
    )
    content: Mapped['ContentOrm'] = relationship(
        back_populates='images'
    )


class TagOrm(Base):
    __tablename__ = 'tag'

    title: Mapped[Optional[str]]
    slug: Mapped[Optional[str]]
    path: Mapped[Optional[str]]

    article: Mapped[list['ArticleOrm']] = relationship(
        back_populates='tags',
        secondary=article_tag
    )


class SourceOrm(Base):
    __tablename__ = 'source'

    city: Mapped[Optional[str]]
    name: Mapped[Optional[str]]
    url: Mapped[Optional[str]]

    article: Mapped['ArticleOrm'] = relationship(
        back_populates='source'
    )
