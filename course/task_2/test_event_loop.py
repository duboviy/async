import unittest
from event_loop import EventLoop


class TestEventLoop(unittest.TestCase):

    def setUp(self):
        self.event_loop = EventLoop()

    def test_call_soon(self):
        loop = self.event_loop
        ret = []
        a = lambda: ret.append('a') or loop.call_soon(b)
        b = lambda: ret.append('b') or loop.call_soon(c)
        c = lambda: ret.append('c') or loop.call_soon(finish)
        finish = lambda: ret.append('finish') or loop.stop()
        loop.call_soon(a)
        loop.call_soon(a)
        loop.call_soon(lambda: ret.append('d'))
        loop.start()
        self.assertListEqual(['a', 'a', 'd', 'b', 'b',
                              'c', 'c', 'finish', 'finish'], ret)

    def test_call_later(self):
        loop = self.event_loop
        ret = []
        a = lambda: ret.append('a') or loop.call_soon(finish)
        b = lambda: ret.append('b')
        c = lambda: ret.append('c')
        d = lambda: ret.append('d')
        finish = lambda: ret.append('finish') or loop.stop()
        loop.call_later(.1, a)
        loop.call_later(.04, b)
        loop.call_later(.02, d)
        loop.call_later(.07, c)
        loop.start()
        self.assertListEqual(['d', 'b', 'c', 'a', 'finish'], ret)

    def test_cancel(self):
        loop = self.event_loop
        ret = []
        a = lambda: ret.append('a')
        b = lambda: ret.append('b')
        finish = lambda: ret.append('finish') or loop.stop()
        loop.call_soon(a).cancel()
        loop.call_later(.03, b).cancel()
        loop.call_later(.07, finish)
        loop.start()
        self.assertListEqual(['finish'], ret)


if __name__ == '__main__':
    unittest.main()
