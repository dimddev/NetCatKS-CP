__author__ = 'dimd'

from zope.interface import Interface, Attribute


class IStorageRegister(Interface):

    components = Attribute("keep registered components")
    interfaces = Attribute("keep registered interfaces")
