__author__ = 'dimd'

from twisted.python import log
from zope.interface import implementer
from NetCatKS.Logger.api.interfaces import ILogger


GLOBAL_DEBUG = True


@implementer(ILogger)
class Logger(object):

    def __init__(self):
        pass

    def debug(self, msg):

        if GLOBAL_DEBUG is True:
            log.msg('[ ====== DEBUG ]: {}'.format(msg))

    def info(self, msg):
        log.msg('[ ++++++ INFO ]: {}'.format(msg))

    def warning(self, msg):
        log.msg('[ !!!!!! WARNING ]: {}'.format(msg))

    def error(self, msg):
        log.msg('[ ------ ERROR ]: {}'.format(msg))

    def critical(self, msg):
        log.msg('[ @@@@@@ CRITICAL ]: {}'.format(msg))


__all__ = [
    'Logger'
]