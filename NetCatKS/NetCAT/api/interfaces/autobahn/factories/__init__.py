__author__ = 'dimd'


from zope.interface import Interface, Attribute


class IDefaultAutobahnFactory(Interface):

    protocol = Attribute('WAMP protocol can be ws or wss')
    name = Attribute('Service name')
    port = Attribute('WAMP port usually crossbar WS')
    host = Attribute('WAMP host')
    path = Attribute('WAMP path for example: ws://localhost/path')
    realm = Attribute('WAMP Realm')


class IDefaultWSFactory(Interface):

    protocol = Attribute('WS protocol can be ws or wss')
    name = Attribute('Service name')
    port = Attribute('WS port usually crossbar WS')
    host = Attribute('WS host')
    path = Attribute('WS path for example: ws://localhost/path')
    realm = Attribute('WS Realm')


class IDefaultUserWSFactory(Interface):

    protocol = Attribute('A User WS protocol can be ws or wss')
    name = Attribute('A User Service name')
    port = Attribute('A User WS port usually crossbar WS')
    host = Attribute('A User WS host')
    path = Attribute('A User WS path for example: ws://localhost/path')
    realm = Attribute('A User WS Realm')
