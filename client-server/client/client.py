import sys
import time
import platform

from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineReceiver

"""
 epoll is a Linux-only feature. twisted.internet.epollreactor is only
 usable on Linux. You should probably remove the explicit reactor
 selection from the code you're trying to run. Twisted will make a
 reasonable guess about what reactor is best to use on the platform you
 happen to be using if you just import twisted.internet.reactor. Failing
 that, twisted has command-line arguments to allow the user to make an
 explicit reactor selection.
"""
if not platform.system() == 'Windows':
    from twisted.internet import epollreactor
    epollreactor.install()

from twisted.internet import reactor

max_clients_amount = 50000
host = '127.0.0.1'
port = 8001
output_file = sys.stdout   # open( 'log.dat', 'w')


class GlobalStats(object):
    connections = 0
    crefuse = 0
    closed = 0

    def enchant(self):
        self.connections += 1

    def refuse(self):
        self.crefuse += 1

    def lost(self):
        self.closed += 1


gs = GlobalStats()


class EchoClient(LineReceiver):

    measure = True

    def connectionMade(self):
        self.sendLine("Hello, world!")
        print 'connectionMade'
        self.start_time = time.time()

    def lineReceived(self, line):
        if self.measure:
            self.finish_time = time.time() - self.start_time
            output_file.write('%s    %s    %s    %s    %s\n' % (gs.connections + 1,
                                                                self.finish_time,
                                                                gs.crefuse,
                                                                gs.closed,
                                                                line))
            self.measure = False
            if gs.connections + 1 < max_clients_amount:
                gs.enchant()
                reactor.connectTCP(host, port, EchoClientFactory())
            else:
                self.transport.loseConnection()


class EchoClientFactory(ClientFactory):
    protocol = EchoClient

    def clientConnectionFailed(self, connector, reason):
        gs.refuse()

    def clientConnectionLost(self, connector, reason):
        gs.lost()


def main():
    f = EchoClientFactory()
    reactor.connectTCP(host, port, f)
    reactor.run()
    output_file.close()


if __name__ == '__main__':
    main()
