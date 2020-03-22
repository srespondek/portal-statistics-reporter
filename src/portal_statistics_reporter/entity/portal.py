from abc import ABCMeta, abstractmethod
from typing import List, Tuple

from bs4 import BeautifulSoup

from ..utils import get_logger

logger = get_logger(__name__)


class PortalBase(metaclass=ABCMeta):
    @abstractmethod
    def get_most_popular_content(self, category: str, subcategory: str, html_parsed_obj: BeautifulSoup):
        pass

    @abstractmethod
    def generate_mapping(self):
        pass

    @staticmethod
    def _get_topic(bs_obj: BeautifulSoup):
        pass

    @abstractmethod
    def _get_link(self, bs_obj: BeautifulSoup):
        pass


class IMDB(PortalBase):
    url = "https://www.imdb.com"
    subcategories = [
        'thriller',
        'action',
        'horror',
        'music',
        'western',
        'mystery',
        'fantasy',
        'sci-fi'
    ]
    categories = ["tv_series", "movies"]
    processed = False

    def _get_title_type(self, title_type: str) -> str:
        if title_type == 'tv_series':
            return 'tv_series,mini_series'
        elif title_type == 'movies':
            return 'feature'

    def generate_mapping(self) -> Tuple:
        for subcategory in self.subcategories:
            for category in self.categories:
                title_type = self._get_title_type(category)
                url = self._set_url(title_type, subcategory)
                yield category, subcategory, url

    def _set_url(self, title_type: str, genre_type: str) -> str:
        return f"{self.url}/search/title/?genres={genre_type}&title_type={title_type}&explore=genres"

    @staticmethod
    def _get_topic(bs_obj: BeautifulSoup) -> BeautifulSoup:
        return bs_obj.find('a').string

    def _get_link(self, bs_obj: BeautifulSoup) -> BeautifulSoup:
        return self.url + bs_obj.find('a')['href']

    def get_most_popular_content(self, category: str, subcategory: str, html_parsed_obj: BeautifulSoup) -> List:
        bs_obj = html_parsed_obj.findAll(class_='lister-item-content')
        content_list = []
        for content_row in bs_obj:
            topic = self._get_topic(content_row)
            link = self._get_link(content_row)
            logger.debug(f"Current processing data {topic}-{category}-{subcategory}-{link}")
            content_list.append([topic, category, subcategory, link])

        return content_list


class Steam(PortalBase):
    url = "https://store.steampowered.com/"
    subcategories = [
        'Action',
        'Racing',
        'FreeToPlay',
        'Strategy',
        'Sports',
        'Simulation',
        'RPG',
        'Casual',
        'Adventure'
    ]
    categories = ['game']
    processed = False

    def generate_mapping(self):
        for subcategory in self.subcategories:
            for category in self.categories:
                url = self._set_url(subcategory)
                yield category, subcategory, url

    def _set_url(self, genre_type: str) -> str:
        return f"{self.url}/tags/en/{genre_type}/"

    @staticmethod
    def _get_topic(bs_obj: BeautifulSoup) -> BeautifulSoup:
        return bs_obj.find(class_='tab_item_name').string

    def _get_link(self, bs_obj: BeautifulSoup) -> BeautifulSoup:
        return bs_obj.get('href')

    def get_most_popular_content(self, category: str, subcategory: str, html_parsed_obj: BeautifulSoup) -> List:
        content_list = []
        bs_obj = html_parsed_obj.find(class_='tabarea').find(class_='tab_content_ctn sub').find(
            id='tab_content_ConcurrentUsers').find(id='ConcurrentUsersTable').find(id='ConcurrentUsersRows').find_all(
            class_='tab_item')

        for row_index in range(len(bs_obj)):
            content_row = bs_obj[row_index]
            topic = self._get_topic(content_row)
            link = self._get_link(content_row)
            logger.debug(f"Current processing data {topic}-{category}-{subcategory}-{link}")
            content_list.append([topic, category, subcategory, link])

        return content_list