__author__ = 'dimd'

from zope.interface import implementer
from zope.component import getGlobalSiteManager
from zope.component.factory import Factory
from zope.component.interfaces import IFactory

from NetCatKS.DProtocol.api.public.actions import BaseProtocolActions
from NetCatKS.Config.api.interfaces import IWamp


@implementer(IWamp)
class WAMP(BaseProtocolActions):

    def __init__(self):

        self.__user = 'wamp_cra_username'
        self.__password = 'wamp_cra_password'
        self.__service_name = 'wamp service name'
        self.__url = 'ws://localhost:8080/ws'
        self.__realm = 'realm1'
        self.__port = 8080
        self.__protocol = 'ws'
        self.__retry_interval = 2
        self.__path = 'ws'
        self.__hostname = 'localhost'

    @property
    def user(self):
        return self.__user

    @user.setter
    def user(self, user):
        self.__user = user

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, password):
        self.__password = password

    @property
    def service_name(self):
        return self.__service_name

    @service_name.setter
    def service_name(self, name):
        self.__service_name = name

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, url):
        self.__url = url

    @property
    def realm(self):
        return self.__realm

    @realm.setter
    def realm(self, realm):
        self.__realm = realm

    @property
    def port(self):
        return self.__port

    @port.setter
    def port(self, port):
        self.__port = port

    @property
    def protocol(self):
        return self.__protocol

    @protocol.setter
    def protocol(self, protocol):
        self.__protocol = protocol

    @property
    def retry_interval(self):
        return self.__retry_interval

    @retry_interval.setter
    def retry_interval(self, interval):
        self.__retry_interval = interval

    @property
    def path(self):
        return self.__path

    @path.setter
    def path(self, path):
        self.__path = path

    @property
    def hostname(self):
        return self.__hostname

    @hostname.setter
    def hostname(self, host):
        self.__hostname = host

gsm = getGlobalSiteManager()

factory = Factory(WAMP, WAMP.__name__)
gsm.registerUtility(factory, IFactory, WAMP.__name__.lower())