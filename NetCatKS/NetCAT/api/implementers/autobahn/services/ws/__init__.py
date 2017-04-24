__author__ = 'dimd'

from twisted.application import internet, service
from twisted.internet import ssl

from zope.interface import classImplementsOnly
from zope.component import adapts
from zope.component import getGlobalSiteManager

from NetCatKS.NetCAT.api.interfaces.autobahn.services import IDefaultWSService
from NetCatKS.NetCAT.api.interfaces.autobahn.factories import IDefaultWSFactory
from NetCatKS.Logger import Logger

from autobahn.twisted.websocket import listenWS


class DefaultWSService(service.Service):
    """
    Provides functionality for starting default TCP Server as single app or as part of many services
    """
    adapts(IDefaultWSFactory)

    def __init__(self, factory):
        """

        :param factory:
        :type IDefaultFactory

        """

        self.factory = factory

        self.__logger = Logger()

        self.listener = None

        if self.factory.ws_protocol == 'wss':

            self.__ssl_context = ssl.DefaultOpenSSLContextFactory(
                self.factory.crt_keys.get('key'),
                self.factory.crt_keys.get('crt')
            )

        self.setName(self.factory.name)

        if self.factory.belong_to is False:

            self.__application = service.Application(self.factory.name, uid=1000, gid=1000)
            self.service_collection = service.IServiceCollection(self.__application)

        else:

            self.service_collection = self.factory.belong_to

    def startService(self):

        """
        Starting a TCP server and put to the right service collection

        :return:
        """
        if self.factory.ws_protocol == 'ws':

            factory = self.factory.ws_server_factory(self.factory.url)
            factory.protocol = self.factory.ws_msg_protocol
            factory.name = self.factory.name

            self.factory.ws_server_factory = factory

            internet.TCPServer(
                self.factory.port,
                factory,
                50
            ).setServiceParent(self.service_collection)

        else:

            factory = self.factory.ws_server_factory(self.factory.url)

            factory.protocol = self.factory.ws_msg_protocol

            factory.startFactory()

            self.factory.ws_server_factory = factory

            self.listener = listenWS(self.factory.ws_server_factory, self.__ssl_context)

        if self.factory.belong_to is False:

            return self.__application

    def start(self):

        self.setServiceParent(self.service_collection)

        if self.factory.belong_to is False:
            return self.__application

    def stopService(self):

        self.factory.ws_server_factory.stopFactory()

        # if is not meaning wss server
        if self.listener is not None:
            self.listener.stopListening()

classImplementsOnly(DefaultWSService, IDefaultWSService)

gsm = getGlobalSiteManager()
gsm.registerAdapter(DefaultWSService)


__all__ = [
    'DefaultWSService'
]
