__author__ = 'dimd'

from NetCatKS.NetCAT.api.interfaces.twisted.protocols.linereceiver import IDefaultLineReceiver

from NetCatKS.Dispatcher import IDispatcher, DispathcherResultHelper
from NetCatKS.Validators import Validator
from NetCatKS.Logger import Logger

from twisted.protocols.basic import LineReceiver
from zope.interface import implementer


@implementer(IDefaultLineReceiver)
class DefaultLineReceiver(LineReceiver):

    def __init__(self):

        self.__logger = Logger()

    def connectionMade(self):

        self.__logger.info('Connections made')

    def connectionLost(self, reason='unexpected'):

        self.__logger.info('Connection was closesd: {}'.format(reason))

    def lineReceived(self, line):

        self.__logger.info('Received line: {}'.format(line))

        result = IDispatcher(Validator(line)).dispatch()
        result_helper = DispathcherResultHelper(result)

        result_helper.result_validation(
            self.sendLine,
            self.transport.loseConnection,
            'TCP'
        )