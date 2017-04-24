__author__ = 'dimd'

from zope.interface import Interface


class IRegisterProtocols(Interface):

    def register(**kwargs):
        """
        Register Sessions inside zope GSM
        :param kwargs:
        :return:
        """
