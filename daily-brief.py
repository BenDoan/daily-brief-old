#!/usr/bin/env python

import argparse
import json
import os
import urllib

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

WEATHER_URL = "https://api.weather.gov/points/41.252363,-95.997988/forecast"


@get('/')
def index():
    return template("index.tpl", title="index")


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


def main():
    pass


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

    run(host='0.0.0.0', port=config['port'])

app = default_app()

