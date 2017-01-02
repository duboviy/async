#!/usr/local/bin/python3.3
import socket
from threading import Thread
import logging as log
from queue import Queue

WORKER_COUNT = 5
TIMEOUT = 5.
ADDRESS = ('127.0.0.1', 7771)


def worker(num, queue):
    while True:
        sock = queue.get(block=True)
        if sock is None:
            return
        sock.settimeout(TIMEOUT)
        _buffer = b''
        try:
            while b'\n' not in _buffer:
                _buffer += sock.recv(4096)
            msg = _buffer[:_buffer.index(b'\n')]
            log.info("Received message '%s'", msg.decode('utf-8'))
            sock.sendall(b'Echo: ' + msg + b'\n')
        except OSError:
            log.exception('Exception in worker:')


def run_server():
    queue = Queue()
    workers = [Thread(target=worker, args=(num, queue))
                    for num in range(WORKER_COUNT)]
    for w in workers:
        w.start()
    log.info("Start server with address %s:%d", *ADDRESS)
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(ADDRESS)
        sock.listen(5)
        while True:
            conn, addr = sock.accept()
            queue.put(conn)
    finally:
        log.info("Stop server")
        for num in range(len(workers)):
            queue.put(None)

    for w in workers:
        w.join()


if __name__ == '__main__':
    log.basicConfig(level=log.INFO, format='%(message)s')
    run_server()
   
