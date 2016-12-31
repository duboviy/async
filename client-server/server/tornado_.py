import errno
import functools
import socket
from tornado import ioloop, iostream

host = ''
port = 8001
clients = []


class Connection(object):

    def __init__(self, connection):
        clients.append(self)
        self.stream = iostream.IOStream(connection)
        self.read()

    def read(self):
        self.stream.read_until('\r\n', self.eol_callback)

    def eol_callback(self, data):
        for c in clients:
            try:
                c.stream.write(str(len(clients))+'\r\n')
            except:
                clients.remove(c)
        self.read()


def connection_ready(sock, fd, events):

    while True:
        try:
            connection, address = sock.accept()
        except socket.error, e:
            if e[0] not in (errno.EWOULDBLOCK, errno.EAGAIN):
                raise
            return
        connection.setblocking(0)

        Connection(connection)

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setblocking(0)
    sock.bind((host, port))
    sock.listen(30000)

    io_loop = ioloop.IOLoop.instance()
    callback = functools.partial(connection_ready, sock)
    io_loop.add_handler(sock.fileno(), callback, io_loop.READ)
    try:
        io_loop.start()
    except KeyboardInterrupt:
        io_loop.stop()
        print("exited cleanly")
