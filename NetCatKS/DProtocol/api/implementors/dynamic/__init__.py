__author__ = 'dimd'

from NetCatKS.DProtocol.api.implementors.actions import BaseProtocolActionsImplementor
from NetCatKS.DProtocol.api.interfaces.dymanic import IDynamicProtocolInterface

from zope.interface import implementer


@implementer(IDynamicProtocolInterface)
class DynamicProtocolImplementor(BaseProtocolActionsImplementor):

    """
    This class provides implementation of `session.interfaces.dynamic.IDynamicSessionInterface`
    Our public class have to inherit from here
    """

    def __init__(self, **kwargs):
        self.__id = None
        super(DynamicProtocolImplementor, self).__init__(**kwargs)

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, _id):
        self.__id = _id
