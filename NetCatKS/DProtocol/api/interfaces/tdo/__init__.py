__author__ = 'dimd'

from zope.interface import Interface


class IDynamicTDO(Interface):

    def to_tdo(in_data):
        """

        :param in_data:
        :return:
        """

