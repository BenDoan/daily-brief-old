#!/usr/bin/env python

import datetime
import re
import sys

try:
    from cookielib import CookieJar
    from urllib2 import build_opener, HTTPCookieProcessor
except ImportError:
    from http.cookiejar import CookieJar
    from urllib.request import build_opener, HTTPCookieProcessor

BASE_URL = "http://fooda.com/linkedinomaha"
URL = "https://app.fooda.com/my?date={}&filterable%5Baccount_id%5D%5B%5D=2212&filterable%5Bmeal_period%5D={}"

IMG_SRC_REGEX = r'<img.*?src="(.*?)".*?/>'


def main():
    if len(sys.argv) > 1:
        meal = sys.argv[1]
    else:
        meal = "Lunch"

    today = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d")
    print(get_menu_img(today, meal))


def get_menu_img(date, meal):
    opener = build_opener(HTTPCookieProcessor(CookieJar()))
    opener.open(BASE_URL)  # set auth cookie
    page = opener.open(URL.format(date, meal)).read().decode("utf-8")

    matches = re.findall(IMG_SRC_REGEX, page)
    for match in matches:
        if '.jpg' in match:
            return match


if __name__ == '__main__':
    main()
