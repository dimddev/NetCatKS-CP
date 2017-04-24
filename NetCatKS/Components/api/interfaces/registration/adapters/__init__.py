__author__ = 'dimd'

from zope.interface import Interface


class IRegisterAdapters(Interface):

    def register_adapters(**kwargs):
        """
        register adapters into zope GSM
        :param kwargs:
        :return:
        """

    def get_multi_adapter(objects, belong_interface):
        """

        :param objects:
        :param belong_interface:
        :return:
        """
