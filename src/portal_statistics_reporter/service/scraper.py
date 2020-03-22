import requests
from bs4 import BeautifulSoup


class RequestDataException(Exception):
    pass


class ScraperService:
    def _request_data(self, url: str) -> requests.models.Response:
        try:
            data = requests.get(url)
            return data
        except Exception as err:
            raise RequestDataException(str(err))

    def get_parsed_html(self, url: str) -> BeautifulSoup:
        raw_data = self._request_data(url)
        html_data = BeautifulSoup(raw_data.text, 'html.parser')
        return html_data
