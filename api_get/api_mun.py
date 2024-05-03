import requests
import backoff


import logging
from datetime import datetime, timedelta, timezone
from typing import Generator


from models.pydantic_mun_model import News, Article, Image


log = logging.getLogger(__name__)


def backof_handler(details):
    log.debug(
        "Backing off {wait:0.1f} seconds after {tries} tries "
        "calling function {target} with args {args} and kwargs "
        "{kwargs}".format(**details)
    )


@backoff.on_exception(backoff.expo,
                      (requests.exceptions.ProxyError,
                       requests.exceptions.SSLError),
                      max_tries=8,
                      on_backoff=backof_handler)
def get_mun_api(link: str) -> dict[str, any]:
    # получаем данные с внутреннего апи и возвращаем в виде dict
    response = requests.get(link)
    if response.status_code == 200:
        return response.json()
    raise ValueError('Ошибка полученния данных с новостного сайта')


def check_actual_date(date: str) -> bool:
    # проверяем дату
    # если дата статьи + 1 день, будеть больше или равно
    # текущей дате, то данная новость нам подходит
    return ((datetime.fromisoformat(date)+timedelta(days=1))
            > datetime.now(tz=timezone.utc))


def get_full_image_link(link, image: Image):
    image.image_90 = (
        link +
        image.
        image_90[1:]
    )
    image.image_800 = (
        link +
        image.
        image_800[1:]
    )
    image.image_250 = (
        link +
        image.
        image_250[1:]
    )
    image.image_1600 = (
        link +
        image.
        image_1600[1:]
    )
    return image


def mun_get_main(link: str) -> Generator[Article, str, None]:
    # основная функция, для работы с апи
    # однотипных новостных порталов
    # получаем ссылку на нновостной портал
    # если апишки нет выбрасываем исключение
    # (см. get_mun_api)
    api_link = link + '/api/site/matters'
    all_news = get_mun_api(api_link)

    # данные приходят в виде {'matters':[data]}
    # проверяем наличие matters, в случае отсутствия
    # выбрасываем ошибку
    if not (all_news.get('matters')):
        raise ValueError('Полученны не корректные данные с сайта {link}')

    for news in all_news['matters']:
        if check_actual_date(news['published_at']):
            current_news = News(**news)
            article = get_mun_api(api_link + current_news.path)
            current_article = Article(**article)
            current_article.site_link = link

            if current_article.image:
                current_article.image = get_full_image_link(
                    link,
                    current_article.image
                )

            current_article.authors = (
                ', '.join(current_article.authors)
                if current_article.authors
                else current_article.authors
                )

            article_content_blocks = current_article.content_blocks
            for content in article_content_blocks:
                content_images = content.images
                if content_images:
                    for index, content_img in enumerate(content_images):
                        content_images[index] = get_full_image_link(
                            link,
                            content_img
                        )
            yield current_article
