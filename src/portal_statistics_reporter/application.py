from typing import List, Union

from src.portal_statistics_reporter.entity.portal import Steam, IMDB
from src.portal_statistics_reporter.service import ScraperService, LocalStorageService
from src.portal_statistics_reporter.utils import get_logger

logger = get_logger(__name__)


class PortalStatisticsReporter:
    MOST_POPULAR_TARGET_LIST = []

    def __init__(self, portal_obj_list: List):
        self.portal_obj_list = portal_obj_list

        self.scraper_service = ScraperService()
        self.local_storage_service = LocalStorageService()

    def _process(self, portal_obj: Union[Steam, IMDB]) -> None:
        logger.info(f"Initializing process data of the {portal_obj.url} web-site")

        portal_obj_gen = portal_obj.generate_mapping()

        for category, subcategory, url in portal_obj_gen:
            html_parsed_obj = self.scraper_service.get_parsed_html(url)
            content = portal_obj.get_most_popular_content(category, subcategory, html_parsed_obj)
            self.MOST_POPULAR_TARGET_LIST.extend(content)
        portal_obj.processed = True
        logger.debug(f"Successfully processed {len(self.MOST_POPULAR_TARGET_LIST)} data")

    def run(self):
        [self._process(website_obj) for website_obj in self.portal_obj_list]
        self.local_storage_service.write_to_csv(self.MOST_POPULAR_TARGET_LIST)

        return 'OK' if all([portal_obj.processed for portal_obj in self.portal_obj_list]) == True else 'Error'
