from bs4 import BeautifulSoup


class Service:
    @staticmethod
    def remove_links(html: str):
        # soup = BeautifulSoup(html, 'lxml')
        # for link in soup.find_all('a'):
        #     link.unwrap()
        # return str(soup)
        return html
