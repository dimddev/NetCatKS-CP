__author__ = 'dimd'

from NetCatKS.Components import IXMLResourceAPI, IXMLResource
from zope.interface import implementer
from zope.component import adapts


@implementer(IXMLResourceAPI)
class Convert(object):

    adapts(IXMLResource)

    def __init__(self, factory):

        self.factory = factory

    def process_factory(self):

        self.factory.convert.id = 42
        return self.factory
