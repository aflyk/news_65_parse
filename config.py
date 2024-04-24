from pydantic_settings import BaseSettings, SettingsConfigDict


from typing import Optional


class Setting(BaseSettings):
    news_link: Optional[list[dict[str, str]]] = []
    headers: dict[str, str] = {
        'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0)'
                       ' Gecko/20100101 Firefox/124.0')
    }

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str

    @property
    def DATABASE_URL_psycopg(self):
        return (f'postgresql+psycopg2://{self.POSTGRES_USER}:'
                f'{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}'
                f':{self.POSTGRES_PORT}/{self.POSTGRES_DB}')

    model_config = SettingsConfigDict(env_file='.env')


settings = Setting()

SOURCE_LIST = [
    'Южно-Сахалинск - Газета «Южно-Сахалинск сегодня» - https://sakhizdat.ru/',
    'Корсаковский ГО - Газета «Восход» - https://восход65.рф/',
    'Долинский ГО - Газета «Долинская правда» - https://dolinsk.today/',
    'Ногликский ГО - Газета «Знамя труда» - https://noglgazeta.ru/',
    'Александровск-Сахалинский - Газета '
    '«Красное знамя» - https://znamya65.ru/',
    'Курильский - Газета «Красный маяк» - https://iturup.news/',
    'Северо-Курильскиий - Газета «Курильский рыбак» — https://krsevkur.ru/',
    'Южно-Курильский - Газета «На рубеже» — https://kurilnews.ru/',
    'Невельский - Газета «Невельские новости» — https://nevnews.info/',
    'Макаровий - Газета «Новая газета» — https://gazetamakarov.ru/',
    'Смирныховский - Газета «Новая жизнь» — https://alsakh.ru/',
    'Тымовский - Газета «Тымовский вестник» — https://tymnews.ru/',
    'Анивский - Газета «Утро Родины» - https://aniva-utro.ru/',
    'Холмский - Газета «Холмская панорама» - https://kholmsk.info/',
    'Попронайский - Газета «Экспресс» - https://express65.ru/',
    'Томаринский - Газета «Вести Томари» - https://vesti-tomari.ru/',
    'Южно-Сахалинск - sahk-online - https://sakh.online/'
]

for source in SOURCE_LIST:
    city, name, url = [_.strip()
                       for _ in source.replace('—', '-').split(' - ')]
    settings.news_link.append(
        {
            'city': city,
            'name': name,
            'url': url,
        }
    )
