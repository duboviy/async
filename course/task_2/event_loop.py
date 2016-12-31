#!/usr/local/bin/python3.3
import time
import heapq
from collections import deque
from functools import total_ordering


class EventLoop(object):

    def __init__(self, selector=None):
        self._running = False
        self._ready = deque()
        self._scheduled = []
        self._selector = selector or Selector()

    def start(self, max_poll_timeout=100.0):
        self._running = True

        while self._running:
            poll_timeout = max_poll_timeout
            ready = self._ready
            self._ready = deque()

            while ready:
                handle = ready.popleft()
                if not handle._cancelled:
                    handle._run()

            scheduled = self._scheduled
            now = self.time()

            while scheduled and scheduled[0]._when <= now:
                handle = heapq.heappop(scheduled)
                if not handle._cancelled:
                    self._ready.append(handle)

            if self._ready:
                poll_timeout = 0

            if scheduled:
                poll_timeout = min(poll_timeout, scheduled[0]._when - now)

            event_list = self._selector.select(poll_timeout)
            self._process_events(event_list)

    def stop(self):
        self._running = False

    def call_soon(self, callback):
        handle = Handle(callback)
        self._ready.append(handle)
        return handle

    def call_later(self, delay, callback):
        when = self.time() + delay
        return self.call_at(when, callback)

    def call_at(self, when, callback):
        handle = TimeHandle(when, callback)
        heapq.heappush(self._scheduled, handle)
        return handle

    def time(self):
        return time.monotonic()

    def _process_events(self, event_list):
        pass


class Handle(object):

    def __init__(self, callback):
        self._callback = callback
        self._cancelled = False

    def __repr__(self):
        state = 'Cancelled' if self._cancelled else 'Active'
        return 'Handle(callback={}). {}'.format(self._callback, state)

    def __bool__(self):
        return not self._cancelled

    def cancel(self):
        self._cancelled = True

    def _run(self):
        try:
            self._callback()
        except Exception:
            pass


@total_ordering
class TimeHandle(Handle):

    def __init__(self, when, callback):
        super().__init__(callback)
        self._when = when

    def __lt__(self, other):
        return self._when < other._when

    def __eq__(self, other):
        return self._when == other._when

    def __repr__(self):
        state = 'Cancelled' if self._cancelled else 'Active'
        return 'Handle(callback={}, when={}). {}'.format(self._callback,
                                                         self._when, state)

class Selector(object):

    def select(self, timeout):
        return tuple()
