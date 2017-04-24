__author__ = 'dimd'

from zope.interface import implementer

from twisted.internet.protocol import Factory
from autobahn.twisted.websocket import WebSocketServerFactory

from NetCatKS.NetCAT.api.interfaces.autobahn.factories import IDefaultWSFactory
from NetCatKS.NetCAT.api.implementers.autobahn.protocols import DefaultWSProtocol
from NetCatKS.Config.api.implementers.configuration.ws import WS
from NetCatKS.Logger import Logger


class DefaultWSFactoryRunner(WebSocketServerFactory):
    def __init__(self, *args, **kwargs):
        super(DefaultWSFactoryRunner, self).__init__(*args, **kwargs)

@implementer(IDefaultWSFactory)
class DefaultWSFactory(object):

    def __init__(self, **kwargs):
        """
        Default factory, used for TCP servers, implements IDefaultFactory
        :param kwargs:
        :return:
        """
        self.__logger = Logger()

        self.config = kwargs.get('config', None)

        if self.config is None:

            ws = WS()

            self.__logger.warning('Config for IDefaultFactory is not provided, failback to defaults...')

            self.config = {
                'url': 'ws://localhost:8585',
                'port': 8585,
                'hostname': 'localhost',
                'protocol': 'ws'
            }

            self.config = ws.to_object(self.config)

        self.ws_protocol = self.config.protocol

        self.name = kwargs.get('name', 'DefaultWSFactory')

        self.port = kwargs.get('port', self.config.port)

        self.url = kwargs.get('port', self.config.url)

        self.belong_to = kwargs.get('belong_to', False)

        self.ws_server_factory = DefaultWSFactoryRunner

        if self.ws_protocol == 'wss':

            key = self.config.keys.key
            crt = self.config.keys.crt

            if key is None or crt is None:
                raise AttributeError('WS over SSL required attribute a key and a crt')

            self.crt_keys = dict(key=key, crt=crt)

        self.ws_msg_protocol = DefaultWSProtocol