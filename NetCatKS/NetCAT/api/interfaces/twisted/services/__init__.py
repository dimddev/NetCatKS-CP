__author__ = 'dimd'

from zope.interface import Interface
from NetCatKS.NetCAT.api.interfaces.twisted.services.web import IDefaultWebService


class IDefaultService(Interface):

    def start():
        """
        Start default service
        :return:
        """

__all__ = [
    'IDefaultService',
    'IDefaultWebService'
]

