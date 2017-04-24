__author__ = 'dimd'

from zope.interface import Interface, Attribute


class ILogger(Interface):

    default = Attribute("default logging module")
    origin = Attribute("Current module")

    def info(msg):
        """
        Info logging level
        :param msg: info message
        """

    def debug(msg):
        """
        debug logging level
        :param msg: debug message
        """

    def error(msg):
        """
        error level loggign
        :param msg: error message
        :return:
        """

    def warning(msg):
        """
        warning level loggign
        :param msg: warrning message
        :return:
        """

    def critical(msg):
        """
        critical logging level
        :param msg:
        :return:
        """
