__author__ = 'dimd'

from NetCatKS.Validators.api.interfaces.message import IMessage
from NetCatKS.Validators.api.implementers.validators.default import BaseValidator

from zope.component import adapts
from zope.component import getGlobalSiteManager

from lxml import etree


class XMLValidator(BaseValidator):

    adapts(IMessage)

    def __init__(self, validate_msg):
        super(XMLValidator, self).__init__(validate_msg)

    def validate(self):

        try:

            __xml = etree.fromstring(self.validate_msg.message)

        except Exception as e:
            return self

        else:

            self.is_valid = True
            self.message_type = 'XML'
            self.message = self.validate_msg.message

            return self

gsm = getGlobalSiteManager()
gsm.registerSubscriptionAdapter(XMLValidator)