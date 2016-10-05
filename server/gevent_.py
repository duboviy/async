clients = []
host = ''
port = 8001


def chat_echo_server(socket, address):
    clients.append(socket)
    while True:
        line = socket.recv(1024)
        for client in clients:
            try:
                client.send(str(len(clients)) + '\r\n')
            except:
                clients.remove(client)


if __name__ == '__main__':
    from gevent.server import StreamServer

    StreamServer((host, port), chat_echo_server).serve_forever()
