from __future__ import absolute_import

__author__ = 'dimd'

from zope.interface import implementer
from zope.component import getGlobalSiteManager
from zope.component.factory import Factory
from zope.component.interfaces import IFactory

from NetCatKS.DProtocol.api.public.actions import BaseProtocolActions
from NetCatKS.Config.api.interfaces import ITcp


@implementer(ITcp)
class TCP(BaseProtocolActions):

    def __init__(self):

        self.__port = 8484
        self.__service_name = 'Default TCP Server'
        self.__tcp_back_log = 50

    @property
    def port(self):
        return self.__port

    @port.setter
    def port(self, port):
        self.__port = port

    @property
    def service_name(self):
        return self.__service_name

    @service_name.setter
    def service_name(self, name):
        self.__service_name = name

    @property
    def tcp_back_log(self):
        return self.__TCP_BACK_LOG

    @tcp_back_log.setter
    def tcp_back_log(self, back_log):
        self.__tcp_back_log = back_log


gsm = getGlobalSiteManager()

factory = Factory(TCP, TCP.__name__)
gsm.registerUtility(factory, IFactory, TCP.__name__.lower())