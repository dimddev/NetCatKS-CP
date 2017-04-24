__author__ = 'dimd'


from zope.interface import Interface, Attribute


class IDefaultWebService(Interface):

    factory = Attribute('attribute that will adapt IDefaultWebFactory')

    def get_service():
        """
        return web root
        :return:
        """

    def start():
        """
        start default web service
        :return:
        """

