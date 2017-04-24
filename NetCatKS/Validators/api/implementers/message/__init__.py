__author__ = 'dimd'

from zope.interface import implementer
from NetCatKS.Validators.api.interfaces.message import IMessage


@implementer(IMessage)
class Message(object):

    def __init__(self, message):
        self.message = message
