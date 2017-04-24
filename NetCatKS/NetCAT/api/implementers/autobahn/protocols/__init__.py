__author__ = 'dimd'

from zope.interface import implementer
from autobahn.twisted.websocket import WebSocketServerProtocol

from NetCatKS.NetCAT.api.interfaces import IWSProtocol
from NetCatKS.Dispatcher import IDispatcher, DispathcherResultHelper
from NetCatKS.Validators import Validator
from NetCatKS.Logger import Logger

logger = Logger()


@implementer(IWSProtocol)
class DefaultWSProtocol(WebSocketServerProtocol):

    def onConnect(self, request):
        logger.info("Client connecting: {0}".format(request.peer))

    def onOpen(self):
        logger.info("WebSocket connection open.")

    def onMessage(self, payload, is_binary):

        if is_binary:

            logger.info("Binary message received: {0} bytes".format(len(payload)))
            self.dropConnection('not supported')

        else:

            result = IDispatcher(Validator(payload.decode('utf8'))).dispatch()
            result_helper = DispathcherResultHelper(result)

            result_helper.result_validation(
                self.sendMessage,
                self.dropConnection,
                'WS'
            )

    def onClose(self, was_clean, code, reason):

        logger.info("WebSocket connection closed: {0}".format(reason))