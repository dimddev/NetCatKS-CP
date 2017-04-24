
from __future__ import absolute_import

from zope.interface import Interface, Attribute, implementer

from NetCatKS.DProtocol import BaseProtocolActions
from NetCatKS.Components import IJSONResource, RequestSubscriber

__author__ = 'NetCatKS auto generator at 2015-10-02 16:03:11.224681'


class ITimeInterface(Interface):
        
    clock = Attribute("Comments going here")
        

@implementer(ITimeInterface)
class TimeImplementer(BaseProtocolActions):

    def __init__(self, **kwargs):
        
        self.__clock = None
        
    @property
    def clock(self):
        return self.__clock

    @clock.setter
    def clock(self, clock):
        self.__clock = clock
            

@implementer(IJSONResource)
class TimeProtocol(TimeImplementer, RequestSubscriber):

    def __init__(self, **kwargs):
        super(TimeProtocol, self).__init__(**kwargs)