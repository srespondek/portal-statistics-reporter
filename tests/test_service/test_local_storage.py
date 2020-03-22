from unittest import TestCase
from unittest.mock import Mock, patch, mock_open

from src.portal_statistics_reporter.service.local_storage import LocalStorageService


class TestLocalStorageService(TestCase):

    def setUp(self):
        super().setUp()
        self.local_storage_service = LocalStorageService()

        self.mock_writer = patch('src.portal_statistics_reporter.service.local_storage.writer').start()
        self.mock_builtins_open = patch('builtins.open', mock_open()).start()

    def tearDown(self):
        super().tearDown()
        patch.stopall()

    def test_write_csv(self):
        # given
        self.local_storage_service._set_path = Mock(return_value='/test/path')
        self.local_storage_service._get_date = Mock(return_value='20190805')

        # when
        self.local_storage_service.write_to_csv(['test_1', 'test_2', 'test_3', 'test_4'])

        # then
        self.mock_writer.assert_called_once()
