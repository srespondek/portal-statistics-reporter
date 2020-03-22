import os
from unittest import TestCase

from bs4 import BeautifulSoup

from src.portal_statistics_reporter.entity import Steam, IMDB

test_base = os.path.dirname(os.path.realpath(__file__))


class TestPortal(TestCase):
    def setUp(self):
        super().setUp()

        self.steam_portal = Steam()
        self.imdb_portal = IMDB()

    def test_generating_maping_portal_steam(self):
        # given
        self.steam_portal.subcategories = ['test_sub_category_1', 'test_sub_category_2']

        # when
        result = self.steam_portal.generate_mapping()

        # then
        self.assertTupleEqual(
            ('game', 'test_sub_category_1', 'https://store.steampowered.com//tags/en/test_sub_category_1/'),
            next(result)
        )
        self.assertTupleEqual(
            ('game', 'test_sub_category_2', 'https://store.steampowered.com//tags/en/test_sub_category_2/'),
            next(result)
        )

    def test_generating_maping_portal_imdb(self):
        # given
        self.imdb_portal.subcategories = ['test_sub_category_1', 'test_sub_category_2']
        self.imdb_portal.categories = ['test_category_1']

        # when
        result = self.imdb_portal.generate_mapping()

        # then
        self.assertTupleEqual(
            ('test_category_1', 'test_sub_category_1',
             'https://www.imdb.com/search/title/?genres=test_sub_category_1&title_type=None&explore=genres'),
            next(result)
        )
        self.assertTupleEqual(
            ('test_category_1', 'test_sub_category_2',
             'https://www.imdb.com/search/title/?genres=test_sub_category_2&title_type=None&explore=genres'),
            next(result)
        )

    def test_get_most_popular_content_steam(self):
        # given
        with open(os.path.join(test_base, '../test_samples/', 'sample_raw_data_steam.txt'),
                  'r') as sample_steam_raw_file:
            file_content = sample_steam_raw_file.read()

        soup_obj = BeautifulSoup(file_content, 'html.parser')
        expected_first_output_record = [
            'Dota 2', 'test_category_1', 'test_sub_category_1',
            'https://store.steampowered.com/app/570/Dota_2/?snr=1_241_4_action_1454'
        ]

        # when
        result = self.steam_portal.get_most_popular_content('test_category_1', 'test_sub_category_1', soup_obj)

        # then
        self.assertEqual(result[0], expected_first_output_record)

    def test_get_most_popular_content_imdb(self):
        # given
        with open(os.path.join(test_base, '../test_samples/', 'sample_raw_data_imdb.txt'),
                  'r') as sample_steam_raw_file:
            file_content = sample_steam_raw_file.read()

        soup_obj = BeautifulSoup(file_content, 'html.parser')
        expected_output = [
            'Szybcy i wściekli: Hobbs i Shaw', 'test_category_1', 'test_sub_category_1',
            'https://www.imdb.com/title/tt6806448/'
        ]

        # when
        result = self.imdb_portal.get_most_popular_content('test_category_1', 'test_sub_category_1', soup_obj)
        first_row_record = result[0]

        # then
        self.assertEqual(first_row_record, expected_output)
