from __future__ import absolute_import

from zope.interface import Interface, Attribute, implementer

from NetCatKS.DProtocol import BaseProtocolActions
from NetCatKS.Components import IJSONResource, RequestSubscriber

__author__ = 'NetCatKS auto generator at 2015-10-14 14:38:20.745307'
    

class ITimeInterface(Interface):
        
    time = Attribute("Comments going here")
        

@implementer(ITimeInterface)
class TimeImplementer(BaseProtocolActions):

    def __init__(self, **kwargs):
        
        self.__time = None
        
    @property
    def time(self):
        return self.__time

    @time.setter
    def time(self, time):
        self.__time = time
            

@implementer(IJSONResource)
class TimeProtocol(TimeImplementer, RequestSubscriber):

    def __init__(self, **kwargs):

        super(TimeProtocol, self).__init__(**kwargs)
