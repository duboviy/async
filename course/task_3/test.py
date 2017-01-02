#!/usr/local/bin/python3.3
# pip install tulip
import time
import unittest

from unittest.mock import patch
from page_download import get_page


class StrangeHttpError(Exception):
    pass


class Response:

    def read(self):
        return bytearray(b'Mega page')
        yield

    def get_content_charset(self):
        return 'utf-8'


class Request:

    def __init__(self, success_attempt):
        self.success_attempt = success_attempt
        self.current_attempt = 0

    def __call__(self, *args):
        self.current_attempt += 1
        if self.current_attempt == self.success_attempt:
            return Response()
        raise StrangeHttpError
        yield


class TestEventLoop(unittest.TestCase):

    @patch('tulip.http.request', Request(3))
    def test_last_attempt(self):
        start = time.time()
        self.assertEqual('Mega page', get_page('http://site.com'))
        self.assertLessEqual(10, time.time() - start)

    @patch('tulip.http.request', Request(13))
    def test_error(self):
        with self.assertRaises(StrangeHttpError):
            self.assertEqual('Mega page', get_page('http://site.com'))


if __name__ == '__main__':
    unittest.main()
