import logging
import time
from datetime import datetime, timedelta


import requests
from bs4 import BeautifulSoup as bs
from slugify import slugify


from models.pydantic_mun_model import Article


log = logging.getLogger(__name__)


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


def get_article_tags(article_soup: bs) -> list[dict[str, str | None]]:
    tags_list = []
    for tags_block in article_soup.find_all('div', 'block-tegs-text'):
        for tags in tags_block.find_all('a'):
            tag_dict = {
                'title': tags.text,
                'slug': slugify(tags.text.strip()),
                'path': None
            }
            if tag_dict not in tags_list:
                tags_list.append(tag_dict)
    return tags_list


def get_content_img_dict(soup):
    img_link_bs = soup.find('img')
    if not img_link_bs:
        return None
    img_short_link = img_link_bs.get('src')
    img_full_link = 'https://astv.ru' + img_short_link
    return {
            'image_90': img_full_link,
            'image_250': img_full_link,
            'image_800': img_full_link,
            'image_1600': img_full_link,
            'width': img_link_bs.get('width'),
            'height': img_link_bs.get('height'),
        }


def create_content(
        position: int,
        kind: str,
        text: None | str = None,
        images: None | list[dict[str, str | None]] = None
        ) -> dict[str, any]:
    return {
        'position': position,
        'kind': kind,
        'text': text,
        'images': images,
    }


def parse_content(content_page: bs):
    elem_list = content_page.find('div', attrs={'id': 'mainContentFromPage'})
    elem_list_p = elem_list.find_all('p')
    content_list = []

    if elem_list_p:
        for index, elem in enumerate(elem_list_p):
            if elem.find('img'):
                image = get_content_img_dict(elem)
                content_dict = create_content(index, 'image', images=[image])

            elif elem.find('iframe'):
                content_dict = create_content(index, 'video')

            else:
                content_dict = create_content(index, 'common', elem.prettify().strip())

            log.debug(f'вывод {content_dict}')
            content_list.append(content_dict)

    else:
        elem_list_div = elem_list.find_all('div', class_=None)
        img_dict: dict[str, dict[str, str | None | int]] = {}

        for index, elem in enumerate(elem_list_div):
            if elem.find('a'):
                img_gallery_bs = elem.find('a')
                img_link_bs = img_gallery_bs.find('img')
                if not img_link_bs:
                    continue
                img_link = img_link_bs.get('src')
                if not img_dict.get(img_link):
                    img_dict[img_link] = {
                            'image_90': img_link,
                            'image_250': img_link,
                            'image_800': img_link,
                            'image_1600': img_link,
                            'width': img_link_bs.get('width'),
                            'height': img_link_bs.get('height'),
                            'position': index
                        }
            elif elem.find('img'):
                log.debug('обработка фотки')
                image = get_content_img_dict(elem)
                content_dict = create_content(index, 'image', images=[image])
            else:
                if elem.text.strip():
                    content_list.append(create_content(index, 'common', elem.prettify().strip()))
                    log.debug(elem.prettify().strip())
        if img_dict:
            index = min(img_dict.values(), key=lambda x: x['position'])['position']
            content_list.append(create_content(index, 'gallery', None, list(img_dict.values())))

    log.debug(f'Возвращаем контент {content_list}')
    return content_list


def main():
    news_list = get_all_news()
    base_url = 'https://astv.ru'
    log.debug(f'Всего получено новостей: {len(news_list)}')
    for news in news_list:
        article_url = news.find('a').get('href')
        article_img = get_article_image_dict(news.find_all('img')[0])

        log.info('Получения заголовка статьи')
        article_title = news.find_all('a')[-1].text
        log.info(f'Получен заголовок статьи: {article_title}')

        log.info('Получение published_at')
        date_string = news.select_one('span.ico-p:not([class*=" "]):not([title])').text
        published_at = convert_str_to_date(date_string)
        log.info(f'Получен published_at: {published_at}')

        rubric_title = news.find_all('a')[-2].text
        log.info(f'Получены рубрики: {rubric_title}')

        article_response = requests.get(base_url + article_url)
        if article_response.status_code != 200:
            log.warning('Проблема получения контента статьи'
                        f'\nurl={base_url + article_url}'
                        f'\nstatus_code={article_response.status_code}')
        article_soup = bs(article_response.text, 'lxml')

        tags = get_article_tags(article_soup)
        log.info('Тэги получены')

        author = article_soup.find('span', attrs={"itemprop": "author"}).text.strip().split()[-1]
        log.info(f'Автор статьи получен: {author=}')

        content_page = article_soup.find('div', class_='content newsDetails')
        lead = content_page.find('div', class_='h3 lid').text
        log.info(f'Краткое описание получено: {lead=}')

        content_blocks = parse_content(content_page)
        log.info('Контент получен')
        article_dict = {
            'title': article_title,
            'published_at': published_at,
            'lead': lead,
            'rubric_title': rubric_title,
            'type': 'АСТВ',
            'authors': author,
            'tags': tags,
            'content_blocks': content_blocks,
            'image': article_img,
            'site_link': base_url,
        }
        yield Article(**article_dict)


if __name__ == '__main__':
    main()
