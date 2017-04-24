__author__ = 'dimd'

from zope.interface import Interface


class IDispatcher(Interface):

    def dispatch(self):
        """
        Dispatch current message to actual factory
        :return:
        """


class IDispathcherResultHelper(Interface):

    def result_validation(self, sender, drop):
        """

        :param sender:
        :param drop:
        :return:
        """

