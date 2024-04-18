from bs4 import BeautifulSoup as bs
from datetime import datetime


def get_actual_news(content: bs) -> datetime:
    news_date = content.find_all('div', class_='FeedListMatter_meta__r0gFU')
    print(news_date)
    data = get_date_from_string(news_date[0].text)
    return data


def get_date_from_string(value: str) -> datetime:
    return datetime.strptime(value)
