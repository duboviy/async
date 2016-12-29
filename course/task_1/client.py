#!/usr/local/bin/python3.3
import socket
import logging as log
from threading import Thread


CLIENT_COUNT = 15
TIMEOUT = 5.
ADDRESS = ('127.0.0.1', 7771)
MESSAGE = 'Test message from client'


def client(num):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(TIMEOUT)
    log.info("Connect client #{0} to {1[0]}:{1[1]}".format(num, ADDRESS))
    sock.connect(ADDRESS)

    try:
        msg = MESSAGE
        assert '\n' not in msg
        msg += ' #{}'.format(num)
        log.info("Send message '{}'".format(msg))
        msg += '\n'
        sock.sendall(msg.encode('utf-8'))
        _buffer = b''
        while b'\n' not in _buffer:
            _buffer += sock.recv(4096)
        response = _buffer[:_buffer.index(b'\n')].decode('utf-8')
        log.info("Response '{}'".format(response, num))
    finally:
        log.info('Close socket of client #{}'.format(num))
        sock.close()


def main():
    clients = [Thread(target=client, args=(num,)) for num in range(CLIENT_COUNT)]
    for cli in clients:
        cli.start()
    for cli in clients:
        cli.join()

if __name__ == '__main__':
    log.basicConfig(level=log.INFO, format='%(message)s')
    main()
   
