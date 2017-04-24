__author__ = 'dimd'

from zope.interface import Interface


class IRegisterFactories(Interface):

    def register(**kwargs):
        """
        register factory into zope GSM
        :param kwargs:
        :return:
        """
