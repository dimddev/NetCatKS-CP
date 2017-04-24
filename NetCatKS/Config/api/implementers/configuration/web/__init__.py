__author__ = 'dimd'

from zope.interface import implementer
from zope.component import getGlobalSiteManager
from zope.component.factory import Factory
from zope.component.interfaces import IFactory

from NetCatKS.DProtocol.api.public.actions import BaseProtocolActions
from NetCatKS.Config.api.interfaces import IWeb


@implementer(IWeb)
class WEB(BaseProtocolActions):

    def __init__(self):

        self.__service_name = 'Default WEB Server'
        self.__http_methods = ['GET']
        self.__port = 8000
        self.__www_root = ''

    @property
    def service_name(self):
        return self.__service_name

    @service_name.setter
    def service_name(self, sname):
        self.__service_name = sname

    @property
    def http_methods(self):
        return self.__http_methods

    @http_methods.setter
    def http_methods(self, methods):
        self.__http_methods = methods

    @property
    def port(self):
        return self.__port

    @port.setter
    def port(self, port):
        self.__port = port

    @property
    def www_root(self):
        return self.__www_root

    @www_root.setter
    def www_root(self, root):
        self.__www_root = root

gsm = getGlobalSiteManager()

factory = Factory(WEB, WEB.__name__)
gsm.registerUtility(factory, IFactory, WEB.__name__.lower())
