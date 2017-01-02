#!/usr/bin/env python3.4
import logging as log

import asyncio
from aiohttp import get, web

from fibonacci import fibonacci as fib


@asyncio.coroutine
def count(request):
    key = request.match_info['key']
    resp = yield from get('http://127.0.0.1:8080/count/{}'.format(key))
    count = yield from resp.text()
    return web.Response(text=count)


@asyncio.coroutine
def fibonacci(request):
    n = int(request.match_info['n'])
    ans = fib(n)
    return web.Response(text=str(ans))



def main():
    app = web.Application()
    app.router.add_route('GET', r'/count/{key}', count)
    app.router.add_route('GET', r'/fibonacci/{n:\d+}', fibonacci)

    loop = asyncio.get_event_loop()
    handler = app.make_handler()
    f = loop.create_server(handler, '0.0.0.0', 8081)
    srv = loop.run_until_complete(f)
    log.info('serving on %s', srv.sockets[0].getsockname())
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.run_until_complete(handler.finish_connections(1.0))
        srv.close()
        loop.run_until_complete(srv.wait_closed())
        loop.run_until_complete(app.finish())
    loop.close()


if __name__ == '__main__':
    log.basicConfig(level=log.INFO, format='%(message)s')
    main()
