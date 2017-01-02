#!/usr/local/bin/python3.3
import tulip    # pip install tulip

CLIENT_COUNT = 15
ADDRESS = ('127.0.0.1', 7771)
MESSAGE = 'Test message from client'


@tulip.task
def client(num):
    loop = tulip.get_event_loop()
    print("Connect client #{0} to {1[0]}:{1[1]}".format(num, ADDRESS))
    transp, stream = yield from loop.create_connection(
                                tulip.StreamProtocol, *ADDRESS)
    reader = stream.set_parser(tulip.lines_parser())
    try:
        msg = MESSAGE
        assert '\n' not in msg
        msg += ' #{}'.format(num)
        print("Send message '{}'".format(msg))
        msg += '\n'
        transp.write(msg.encode('utf-8'))
        response = (yield from reader.read())[:-1].decode('utf-8')
        print("Response '{}'".format(response, num))
    finally:
        print('Close connection of client #{}'.format(num))
        transp.close()


@tulip.coroutine
def main():
    clients = [client(num) for num in range(CLIENT_COUNT)]
    yield from tulip.wait(clients)


if __name__ == '__main__':
    loop = tulip.get_event_loop()
    loop.run_until_complete(main())
