from src.portal_statistics_reporter.application import PortalStatisticsReporter
from src.portal_statistics_reporter.entity import Steam, IMDB

steam_portal_obj = Steam()
imdb_portal_obj = IMDB()

application = PortalStatisticsReporter(
    [
        steam_portal_obj,
        imdb_portal_obj
    ]
)

def app_handler() -> dict:
    result = application.run()
    status = 200 if result == 'OK' else 499

    return {
        'statusCode': status,
        'Body': result
    }
