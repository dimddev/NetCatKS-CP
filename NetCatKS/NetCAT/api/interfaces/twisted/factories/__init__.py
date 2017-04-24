__author__ = 'dimd'

from zope.interface import Interface, Attribute


class IDefaultFactory(Interface):
    """

    """
    config = Attribute('config as dict')
    protocol = Attribute('Factory used protocol')
    name = Attribute('Name of this service')
    port = Attribute('Port number')


class IDefaultWebFactory(Interface):
    """

    """
    config = Attribute('config as dict')
    name = Attribute('Name of this service')
    port = Attribute('Port number')
    methods = Attribute('A list that contains all allowed methods: GET, POST... etc')


__all__ = [
    'IDefaultFactory',
    'IDefaultWebFactory'
]
