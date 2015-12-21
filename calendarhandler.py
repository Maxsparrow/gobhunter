import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client, tools

import datetime

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Gobhunter'


def _get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-gobhunter.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def get_events(input_date=None):
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    credentials = _get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    # Find date to use
    timezoneoffset = datetime.timedelta(hours=6)

    if input_date:
        date_to_use = datetime.datetime.strptime(input_date, "%Y-%m-%d")
    else:
        date_to_use = datetime.datetime.now() - timezoneoffset
    today_start = datetime.datetime(date_to_use.year, date_to_use.month, date_to_use.day, 0, 0, 1) + timezoneoffset
    today_end = datetime.datetime(date_to_use.year, date_to_use.month, date_to_use.day, 23, 59, 59) + timezoneoffset
    today_start_str = today_start.isoformat() + 'Z' # 'Z' indicates UTC time
    today_end_str = today_end.isoformat() + 'Z' # 'Z' indicates UTC time

    # Get events for date to use
    print "Getting events for %s: " % date_to_use.date()
    eventsResult = service.events().list(
        calendarId='primary', timeMin=today_start_str, timeMax=today_end_str,
        maxResults=10, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    if not events:
        print('No events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print "Got event for %s: %s" % (start, event['summary'])

    return events


if __name__ == '__main__':
    get_events("2015-12-25")
    get_events()
