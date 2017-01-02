#!/usr/local/bin/python3.3
import tulip    # pip install tulip

WORKER_COUNT = 5
TIMEOUT = 5.
ADDRESS = ('127.0.0.1', 7771)


class Server(tulip.StreamProtocol):

    def connection_made(self, transport):
        self.transport = transport
        task = self.process_request()
        self.timeout = tulip.get_event_loop().call_later(TIMEOUT, task.cancel)

    @tulip.task
    def process_request(self):
        try:
            reader = self.set_parser(tulip.lines_parser())
            msg = (yield from reader.read())[:-1]
            self.timeout.cancel()
            print("Received message '{}'".format(msg.decode('utf-8')))
            self.transport.write(b'Echo: ' + msg + b'\n')
        finally:
            self.transport.close()


def run_server():
    loop = tulip.get_event_loop()
    loop.start_serving(Server, *ADDRESS)
    print("Start server with address {0}:{1}".format(*ADDRESS))
    loop.run_forever()
    print("Stop server")


if __name__== '__main__':
    run_server()


