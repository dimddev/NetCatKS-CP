__author__ = 'dimd'

from twisted.application import internet, service

from zope.interface import classImplementsOnly
from zope.component import adapts
from zope.component import getGlobalSiteManager

from NetCatKS.NetCAT.api.interfaces.twisted.services import IDefaultService
from NetCatKS.NetCAT.api.interfaces.twisted.factories import IDefaultFactory
from NetCatKS.NetCAT.api.implementers.twisted.services.web import DefaultWebService


class DefaultService(service.Service):
    """
    Provides functionality for starting default TCP Server as single app or as part of many services
    """
    adapts(IDefaultFactory)

    def __init__(self, factory):
        """

        :param factory:
        :type IDefaultFactory

        """

        self.factory = factory

        if self.factory.belong_to is False:

            self.__application = service.Application(self.factory.name, uid=1000, gid=1000)
            self.service_collection = service.IServiceCollection(self.__application)

        else:

            self.service_collection = self.factory.belong_to

    def start(self):

        """
        Starting a TCP server and put to the right service collection

        :return:
        """
        internet.TCPServer(
            self.factory.port,
            self.factory,
            50
        ).setServiceParent(self.service_collection)

        if self.factory.belong_to is False:

            return self.__application


classImplementsOnly(DefaultService, IDefaultService)

gsm = getGlobalSiteManager()
gsm.registerAdapter(DefaultService)


__all__ = [
    'DefaultService',
    'DefaultWebService'
]
