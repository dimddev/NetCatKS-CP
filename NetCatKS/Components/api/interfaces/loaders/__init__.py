__author__ = 'dimd'

from zope.interface import Interface


class IBaseLoader(Interface):

    def load(self):
        """

        :return:
        """


class IUserFactory(Interface):
    """
    Marker for user Factories
    """


class IUserStorage(Interface):
    """
    Marker for user Storages
    """


class IUserWampComponent(Interface):
    """
    marker for user defined wamp component, usually the implementer have to inherit
    from BaseWampComponent
    """


class IUserGlobalSubscriber(Interface):
    """

    The user Implementation of IUserGlobalSubscriber have to adpatee this interface.
    the user have to implement a factory that provide IUserGlobalSubscriber,
    the IUserGlobalSubscriber subscribe method will fire as actual global subscriber
    callback. The factory also have to adaptee IGlobalSubscribeMessage

    """
    def subscribe():
        """

        :return:
        """


class IJSONResource(Interface):

    """
    Marker for JSON Resource.

    """


class IXMLResource(Interface):
    """
    XML Resource marker
    """