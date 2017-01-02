import time
import zmq  # pip install zmq
from multiprocessing import Process

PUB_PORTS = [7771, 7772, 7773]
SUBSCRIBERS = 2


def pub(num, port):
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://127.0.0.1:{}".format(port))
    time.sleep(.5)
    socket.send('Message from publisher #{}'.format(num).encode('ascii'))


def sub(num, ports):
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.setsockopt(zmq.SUBSCRIBE, b'')
    for port in ports:
        socket.connect("tcp://127.0.0.1:{}".format(port))
    for _ in ports:
        msg = socket.recv().decode('ascii')
        print('Subscriber #{} received: {}'.format(num, msg))


def main():
    pubs = [Process(target=pub, args=(num, p)) for num, p in enumerate(PUB_PORTS)]
    subs = [Process(target=sub, args=(num, PUB_PORTS)) for num in range(SUBSCRIBERS)]
    for p in pubs + subs:
        p.start()
    for p in pubs + subs:
        p.join()


if __name__ == '__main__':
    main()
