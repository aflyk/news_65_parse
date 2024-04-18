from typing import Generator

from config import settings
from api_get.api_mun import mun_get_main
from queries.orm import SyncOrm
from models.pydantic_mun_model import ArticleClear


def main(recreate_table: bool = True) -> None:
    if recreate_table:
        SyncOrm.create_table()
    for type_link, links in settings.news_link.items():
        for link in links:
            if type_link == 'mun':
                article_generator = mun_get_main(link)
                send_to_db(article_generator)
                break
            elif type_link == 'reg':
                pass
            else:
                raise f'Неожиданный тип новостных порталов: {type_link}'


def send_to_db(article_generator: Generator) -> None:
    for article in article_generator:
        article_clear = ArticleClear(**article.model_dump())
        SyncOrm.insert_news_to_db(article_clear.model_dump(), article)
        break


if __name__ == '__main__':
    main()
