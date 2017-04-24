from __future__ import absolute_import


from zope.interface import Interface, Attribute, implementer, classImplementsOnly

from NetCatKS.DProtocol import DynamicProtocol, BaseProtocolActions
from NetCatKS.Dispatcher import IXMLResource
from NetCatKS.Components import IJSONResource, RequestSubscriber

# 1. Define of our sub protocols and its interfaces


class ISubTimeProtocol(Interface):

    time = Attribute("this attribute will hold the time")

# All sub protocols have to inherit from BaseProtocolActions
# the protocol attributes are defined as private and accessible via properties
# this give as a way do check values before __setattr__


@implementer(ISubTimeProtocol)
class SubTimeProtocol(BaseProtocolActions):

    def __init__(self):

        self.__time = None

    @property
    def time(self):
        return self.__time

    @time.setter
    def time(self, time):
        self.__time = time


# 2. Define our main protocol and its interface
class ITimeProtocol(Interface):

    clock = Attribute('object represent time')


# Its our main protocol implementer, that initialize all sub protocols via private attributes
# and operate over it with properties
# All main protocols inherit from DynamicProtocol, it will provide the id attribute, it's required for
# DProtocol.
# this protocol can be describe like:
# {"command": "event", "id": 100, "clock": {"time": 1441439006.931552}}
@implementer(ITimeProtocol)
class TimeProtocolImplementer(DynamicProtocol):

    def __init__(self, **kwargs):

        super(TimeProtocolImplementer, self).__init__(**kwargs)

        self.__clock = SubTimeProtocol()
        self.__command = None

    @property
    def command(self):
        return self.__command

    @command.setter
    def command(self, cmd):
        self.__command = cmd

    @property
    def clock(self):
        return self.__clock

    @clock.setter
    def clock(self, clock):
        self.__clock.time = clock


@implementer(IJSONResource)
class TimeProtocol(TimeProtocolImplementer, RequestSubscriber):

    def __init__(self, **kwargs):

        super(TimeProtocol, self).__init__(**kwargs)


@implementer(IJSONResource)
class TimeConvertProtocol(BaseProtocolActions, RequestSubscriber):
    def __init__(self, **kwargs):

        super(TimeConvertProtocol, self).__init__(**kwargs)
        self.__convert = TimeProtocolImplementer()

    @property
    def convert(self):
        return self.__convert

    @convert.setter
    def convert(self, conv):
        self.__convert = conv


class TimeConvertXMLProtocol(TimeConvertProtocol, RequestSubscriber):

    def __init__(self, **kwargs):
        super(TimeConvertXMLProtocol, self).__init__(**kwargs)


classImplementsOnly(TimeConvertXMLProtocol, IXMLResource)