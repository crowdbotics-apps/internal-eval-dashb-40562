import builtins
import logging
import pprint
from itertools import zip_longest

from google.oauth2 import service_account
from googleapiclient.discovery import build
from django.conf import settings


logger = logging.getLogger(__name__)


class GoogleSheetsRepository:

    @staticmethod
    def execute():
        return main()


def make_dicts(header, values):
    return [dict(zip_longest(header, v, fillvalue=None)) for v in values]


def main():
    # Authenticate the API using the service account credentials
    creds = service_account.Credentials.from_service_account_info(
        info=settings.GOOGLE_SERVICE_ACCOUNT
    )
    service = build('sheets', 'v4', credentials=creds)

    # Get the data from the first sheet as a JSON
    spreadsheet_metadata = service.spreadsheets().get(
        spreadsheetId=settings.SPREADSHEET_ID
    ).execute()

    sheet_name = spreadsheet_metadata['sheets'][2]['properties']['title']
    range_name = f'{sheet_name}!A1:Z'
    sheet_data = (
        service.spreadsheets()
        .values()
        .get(spreadsheetId=settings.SPREADSHEET_ID, range=range_name, alt='json')
        .execute()
    )

    # Return the JSON data
    try:
        keys = sheet_data["values"][0]
        answers = sheet_data["values"][1:]
        zipped = make_dicts(keys, answers)
        return zipped
    except builtins.Exception as err:
        logger.error(f"Error trying to fetch data from Googe API: {err}")

