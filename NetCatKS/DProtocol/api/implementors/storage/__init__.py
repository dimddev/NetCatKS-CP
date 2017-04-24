__author__ = 'dimd'

from NetCatKS.DProtocol.api.interfaces.storage import IProtocolStogareInterface
from zope.interface import implementer


@implementer(IProtocolStogareInterface)
class ProtocolStorageImplementor(object):

    session = {}

    __instance = None

    def __new__(cls):
        """
        we implement singleton patter for our Container to ensure that all commands point to one place

        :param cls:
            self instance
        :return:
            singleton instance
        """

        if ProtocolStorageImplementor.__instance is None:

            ProtocolStorageImplementor.__instance = object.__new__(cls)

        return ProtocolStorageImplementor.__instance
