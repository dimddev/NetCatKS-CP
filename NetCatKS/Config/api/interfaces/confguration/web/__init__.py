__author__ = 'dimd'

from zope.interface import Interface, Attribute


class IWeb(Interface):

    service_name = Attribute('A name of this web service')
    http_methods = Attribute('A List of methods')
    port = Attribute('Port number')
    www_root = Attribute('Web (www) root')

