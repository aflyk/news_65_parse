import logging
import time
from datetime import datetime, timedelta


import requests
from bs4 import BeautifulSoup as bs


logging.basicConfig(
    format="#{levelname:8} {lineno}:{funcName} - {message}",
    style='{'
)
log = logging.getLogger(__name__)
log.setLevel('DEBUG')


def get_article_image_dict(img_bs: bs) -> dict[str, str]:
    return {
        'source': img_bs.get('src'),
        'image_90': img_bs.get('src'),
        'image_250': img_bs.get('src'),
        'image_800': img_bs.get('src'),
        'image_1600': img_bs.get('src'),
        'width': img_bs.get('width'),
        'height': img_bs.get('height'),
        }


def convert_str_to_date(string_time: str) -> datetime | None:
    log.debug(string_time)
    if 'вчера' in string_time:
        current_datetime = datetime.now() - timedelta(days=1)
    elif 'сегодня' in string_time:
        current_datetime = datetime.now()
    else:
        return None
    hours, minutes = map(int, string_time[:-1].split()[-1].split(':'))
    published_at = datetime(
        current_datetime.year,
        current_datetime.month,
        current_datetime.day,
        hours,
        minutes,
        0
        )
    return published_at


def get_all_news():
    actual_news_list = []
    for i in range(1, 10):  # у сайта счетчик идет с 1, обработки запроса 0 нет
        link = f'https://astv.ru/news/main/fresh/{i}'
        response = requests.get(link)
        if response.status_code != 200:
            log.warning(
                'Ошибка полученния данных '
                f'{link} \n{response.text}'
            )

        log.info(f'Получен список новостей со страницы {link}')
        soup = bs(response.text, 'lxml')
        response_news_list = soup.find_all('div', class_='item width-100-tiny')
        for response_news in response_news_list:
            log.info('Проверка актуальности даты')
            date_string = (response_news
                           .select_one(
                               'span.ico-p:not([class*=" "]):not([title])'
                           )
                           .text)
            if not convert_str_to_date(date_string):
                log.info(f'Неактуальные новости {date_string}')
                return actual_news_list
            actual_news_list.append(response_news)
        time.sleep(2)
    return actual_news_list


def main():
    news_list = get_all_news()
    # log.debug(news_list)
    log.debug(len(news_list))


if __name__ == '__main__':
    main()
