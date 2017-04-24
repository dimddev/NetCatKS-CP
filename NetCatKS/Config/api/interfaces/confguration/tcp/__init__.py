__author__ = 'dimd'

from zope.interface import Interface, Attribute


class ITcp(Interface):

    port = Attribute('TCP POST')
    service_name = Attribute('TCP SERVICE NAME')
    tcp_back_log = Attribute('TCP BACK LOG SIZE')




