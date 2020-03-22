from unittest import TestCase
from unittest.mock import patch, MagicMock

from src.portal_statistics_reporter.application import PortalStatisticsReporter


class TestApplication(TestCase):
    def setUp(self):
        super().setUp()
        self.mock_portal = MagicMock()
        self.mock_local_storage = patch('src.portal_statistics_reporter.application.LocalStorageService').start()
        self.mock_scraper_service = patch('src.portal_statistics_reporter.application.ScraperService').start()

        self.application = PortalStatisticsReporter([
            self.mock_portal
        ])

    def tearDown(self):
        super().tearDown()
        patch.stopall()

    def test_data_processing(self):
        # given / when
        self.application.run()

        # then
        self.mock_portal.generate_mapping.assert_called()
        self.mock_local_storage.assert_called()
        self.mock_scraper_service.assert_called()
