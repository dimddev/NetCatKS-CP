__author__ = 'dimd'

from zope.interface import Interface


class IComponentRegistrator(Interface):

    def make(**kwargs):
        """
        combined register component, factories and adapters
        :param kwargs:
        :return:
        """
