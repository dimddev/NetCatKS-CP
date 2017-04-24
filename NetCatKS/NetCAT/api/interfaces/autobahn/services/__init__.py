__author__ = 'dimd'

from zope.interface import Interface


class IDefaultAutobahnService(Interface):

    def start():
        """
        Start default service
        :return:
        """


class IDefaultWSService(Interface):

    def start():
        """
        Start default service
        :return:
        """

__all__ = [
    'IDefaultAutobahnService',
    'IDefaultWSService'
]

