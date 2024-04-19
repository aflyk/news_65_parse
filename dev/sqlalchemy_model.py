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


class ArticleOrm(Base):
    __tablename__ = 'article'

    title: Mapped[str]
    published_at: Mapped[datetime]
    lead: Mapped[str]
    rubric_title: Mapped[str]
    type: Mapped[str]
    authors: Mapped[str]

    source_id: Mapped[int] = mapped_column(
        ForeignKey('source.id', name='fk_article_source')
    )
    image_id: Mapped[int] = mapped_column(
        ForeignKey('image.id', name='fk_article_image')
    )

    content_blocks: Mapped['ContentOrm'] = relationship(
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
    image: Mapped['ImageOrm'] = relationship(
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

    content_id: Mapped[int] = mapped_column(
        ForeignKey('content.id', name='fk_content_image')
    )

    article: Mapped['ArticleOrm'] = relationship(
        back_populates='image'
    )
    content: Mapped['ContentOrm'] = relationship(
        back_populates='image'
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

    city: Mapped[str]
    name: Mapped[str]
    url: Mapped[str]

    article: Mapped['ArticleOrm'] = relationship(
        back_populates='content'
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

#     article: Mapped['ArticleOrm'] = relationship
