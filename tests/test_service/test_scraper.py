import os
from unittest import TestCase
from unittest.mock import patch, MagicMock

from src.portal_statistics_reporter.service.scraper import ScraperService

test_base = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(test_base, '../test_samples/', 'sample_raw_data_steam.txt'),
          'r') as sample_steam_raw_file:
    file_content = sample_steam_raw_file.read()


class MockedRequest:
    text = file_content


class TestScraperService(TestCase):
    def setUp(self):
        super().setUp()
        self.scraper_service = ScraperService()

        self.mock_bs = patch('src.portal_statistics_reporter.service.scraper.BeautifulSoup').start()

    def tearDown(self):
        super().tearDown()
        patch.stopall()

    def test_get_parsed_html(self):
        # given
        self.scraper_service._request_data = MagicMock(return_value=MockedRequest)

        # when
        self.scraper_service.get_parsed_html(url='http://test.url')

        # then
        self.mock_bs.assert_called_once()
