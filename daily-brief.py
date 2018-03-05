#!/usr/bin/env python

import argparse
import datetime
import json
import os

import feedparser
import httplib2
import requests

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

from lib.bottle import (
    default_app,
    get,
    hook,
    request,
    route,
    run,
    static_file,
    template,
    TEMPLATE_PATH,
)

from get_menu_img import get_menu_img

WEATHER_URL = "https://api.weather.gov/points/41.252363,-95.997988/forecast"

SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'private/client_id.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


@get('/')
def index():
    events = get_events()
    weather_data = get_weather_data()
    menu_img_url = get_menu_url()
    return template(
        "index.tpl",
        title="index",
        weather_data=weather_data,
        events=events,
        menu_img_url=menu_img_url
    )


@route('/static/<path:path>')
def static(path):
    return static_file(path, root=get_script_rel_path("static"))


def get_script_rel_path(filepath):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(script_dir, filepath)


# remove ending slash from requests
@hook('before_request')
def strip_path():
    request.environ['PATH_INFO'] = request.environ['PATH_INFO'].rstrip('/')


def get_weather_data():
    return requests.get(WEATHER_URL).json()


def get_credentials():
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
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = "daily-brief"
        credentials = tools.run_flow(flow, store, None)
        print('Storing credentials to ' + credential_path)
    return credentials


def get_menu_url():
    today = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d")
    return get_menu_img(today, "Lunch")


def get_events():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    eventsResult = service.events().list(
        calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    return events


tpl_path = os.path.join(get_script_rel_path("templates"))
TEMPLATE_PATH.insert(0, tpl_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='starts a lists server')
    parser.add_argument(
        '--config',
        help='specifies the config file location (default: ./config.json)',
        default="./config.json"
    )
    args = parser.parse_args()

    with open(args.config) as f:
        config = json.load(f)

    run(host='0.0.0.0', port=config['port'], reloader=True)

app = default_app()

