__author__ = 'dimd'

from twisted.web.resource import Resource
from twisted.web.server import Site
from twisted.application import service, internet

from NetCatKS.NetCAT.api.implementers.twisted.resources import DefaultWebResource, IDefaultWebResource
from NetCatKS.NetCAT.api.interfaces.twisted.services import IDefaultWebService
from NetCatKS.NetCAT.api.interfaces.twisted.factories import IDefaultWebFactory

from zope.interface import classImplementsOnly
from zope.component import adapts, getGlobalSiteManager


class DefaultWebService(service.Service):

    """

    Will starting default Web server supporting dispatching and validation internally

    """
    adapts(IDefaultWebFactory)

    def __init__(self, factory):
        """

        :param factory:
        :type IDefaultWebFactory

        """

        self.factory = factory

        if self.factory.belong_to is False:

            self.__application = service.Application(self.factory.name, uid=1000, gid=1000)
            self.service_collection = service.IServiceCollection(self.__application)

        else:

            self.service_collection = self.factory.belong_to

    def get_service(self):

        """
        Attach to main web root on default child based on configuration and pass the implementation of
        IDefaultWebResource to it.

        :return: root of ``Resource``
        """
        root = Resource()

        root.putChild(
            self.factory.config.www_root,
            IDefaultWebResource(self.factory)
        )

        return root

    def start(self):

        """
        Starting web server

        :return:
        """

        internet.TCPServer(
            self.factory.port,
            Site(self.get_service()),
            50
        ).setServiceParent(self.service_collection)

        if self.factory.belong_to is False:

            return self.__application


classImplementsOnly(DefaultWebService, IDefaultWebService)

gsm = getGlobalSiteManager()
gsm.registerAdapter(DefaultWebService)


__all__ = [
    'DefaultWebResource'
]
