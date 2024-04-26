import time
import logging.config

from typing import Generator

from log.logging_settings import logging_config
from config import settings
from api_get.api_mun import mun_get_main
from queries.orm import SyncOrm
from models.pydantic_mun_model import ArticleBase


logging.config.dictConfig(logging_config)
log = logging.getLogger(__name__)


def main(recreate_table: bool = True) -> None:
    if recreate_table:
        log.debug('Подготовка базы данных')
        SyncOrm.create_table()
        log.debug('Начало заполнения каталогов')
        SyncOrm.fill_catalog(settings.news_link)
    for source in settings.news_link:
        # добавить проверку нетиповых сайтов(у которых другой апи или его нет)
        article_generator = mun_get_main(source['url'])
        send_to_db(article_generator)
        time.sleep(2)


def send_to_db(article_generator: Generator) -> None:
    for article in article_generator:
        article_clear = ArticleBase(**article.model_dump())
        SyncOrm.insert_news_to_db(article_clear.model_dump(), article)


if __name__ == '__main__':
    start = time.time()
    main(True)
    print(time.time() - start)
