__author__ = 'dimd'

from zope.interface import Interface, Attribute


class IDefaultWebResource(Interface):
    """
    marker for IDefaultWebResource
    """


class IUserPostResource(Interface):

    request = Attribute('Resource from type request')

    def process():
        """

        :return:
        """