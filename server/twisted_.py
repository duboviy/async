import sys
import platform

from twisted.protocols import basic


port = 8001
output_file = sys.stdout   # open( 'log.dat', 'w')


class ChatEchoServer(basic.LineReceiver):

        def connectionMade(self):
            self.factory.clients.append(self)

        def connectionLost(self, reason):
            self.factory.clients.remove(self)

        def dataReceived(self, line):
            output_file.write("dataReceived: %s" % line)
            for c in self.factory.clients:
                c.message(str(len(factory.clients))+'\r\n')

        def message(self, message):
            output_file.write("message %s" % message)
            self.transport.write(message)

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

from twisted.internet import reactor, protocol


factory = protocol.ServerFactory()
factory.protocol = ChatEchoServer
factory.clients = []

reactor.listenTCP(port, factory)
reactor.run()

output_file.close()
