#!/usr/local/bin/python3.3
import tulip    # pip install tulip

from tulip.tasks import sleep
from tulip import http


URL = 'http://www.google.com.ua'
TIMEOUT = 30
ATTEMPTS = 3
ATTEMPT_PAUSE = 5


def do_requests(url):
    for i in range(ATTEMPTS):
        try:
            resp = yield from http.request('GET', url)
            page = yield from resp.read()
            return page.decode(resp.get_content_charset())
        except Exception as e:
            if i == ATTEMPTS - 1:
                raise e
            yield from sleep(ATTEMPT_PAUSE)


def get_page(url):
    loop = tulip.get_event_loop()
    return loop.run_until_complete(do_requests(url))


if __name__ == '__main__':
    print(get_page(URL))
