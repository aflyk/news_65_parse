from pydantic_settings import BaseSettings, SettingsConfigDict


class Setting(BaseSettings):
    news_link: dict[str, list[str]] = {
        'reg': [],
        'mun': [
            'https://sakhizdat.ru/',
            'https://восход65.рф/',
            'https://dolinsk.today/',
            'https://noglgazeta.ru/',
            'https://znamya65.ru/',
            'https://iturup.news/',
            'https://krsevkur.ru/',
            'https://kurilnews.ru/',
            'https://nevnews.info/',
            'https://gazetamakarov.ru/',
            'https://alsakh.ru/',
            'https://tymnews.ru/',
            'https://aniva-utro.ru/',
            'https://kholmsk.info/',
            'https://express65.ru/',
            'https://vesti-tomari.ru/',
        ]
    }
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
print(settings.DATABASE_URL_psycopg)
