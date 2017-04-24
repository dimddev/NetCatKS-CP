__author__ = 'dimd'

from NetCatKS.Components.api.interfaces.storages import IStorageRegister

from zope.interface import implementer
from zope.component.factory import Factory
from zope.component.interfaces import IFactory
from zope.component import getGlobalSiteManager


@implementer(IStorageRegister)
class StorageRegisterImplementer(object):

    __instance = None
    components = {}
    interfaces = {}

    def __new__(cls):
        """
        we implement singleton patter for our Container to ensure that all commands point to one place

        :param cls:
            self instance
        :return:
            singleton instance
        """

        if StorageRegisterImplementer.__instance is None:

            StorageRegisterImplementer.__instance = object.__new__(cls)

        return StorageRegisterImplementer.__instance


class StorageRegister(StorageRegisterImplementer):

    def __init__(self):
        super(StorageRegister, self).__init__()


gsm = getGlobalSiteManager()

factory = Factory(StorageRegister, StorageRegister.__name__)
gsm.registerUtility(factory, IFactory, StorageRegister.__name__.lower())

__all__ = ['StorageRegister']