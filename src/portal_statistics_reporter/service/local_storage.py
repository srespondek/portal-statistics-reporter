import os
from csv import writer
from datetime import datetime
from typing import List


class CSVWriteException(Exception):
    pass


class LocalStorageService:
    headers = ['topic', 'category', 'subcategory', 'url']

    def _set_path(self) -> str:
        current_date = self._get_date()
        return os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../../reports/',
                            f'{str(current_date)}-report.csv')

    def _get_date(self) -> str:
        return datetime.today().strftime('%Y%m%d')

    def write_to_csv(self, target_list: List) -> None:
        path = self._set_path()

        try:
            with open(path, 'w') as csv_file:
                csv_writer = writer(csv_file)
                csv_writer.writerow(self.headers)
                for x in target_list:
                    csv_writer.writerow(x)
        except Exception as err:
            raise CSVWriteException(str(err))
