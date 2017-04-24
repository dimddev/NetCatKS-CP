__author__ = 'dimd'

from zope.interface import Interface, Attribute


class IBaseResourceSubscriber(Interface):

    """

    IBaseResourceSubscriber provides functionality for comparison of the signature on
    a incoming request against a candidate DProtocol implementation registered as
    IJSONResource

    The `adapter` is our first argument in the constructor. It's used from the adapter pattern
    and have to be from type IJSONResource

    The `protocol` attribute is designed to be provided by classes which are implements IJSONResourceSubscriber,
    or inherit from DProtocolSubscriber. If subclass does not provide the protocol argument will
    raise AttributeError.

    """

    adapter = Attribute("The implementer have to provide implementation of IJSONResource")
    protocol = Attribute("DProtocol instance")

    def compare():
        """
        Designed to compare the the adapter and the DProtocol signature
        if the signatures is equal
        """


class IJSONResourceSubscriber(Interface):
    """

    """


class IXMLResourceSubscriber(Interface):
    """

    """