from NetCatKS.Components.api.interfaces.registration.wamp import IWAMPComponent, IWAMPResource
from zope.interface import implementer
from zope.component import adapts

__author__ = 'dimd'


@implementer(IWAMPComponent)
class BaseWampComponent(object):

    adapts(IWAMPResource)

    def __init__(self):

        super(BaseWampComponent, self).__init__()
        self.session = None

    def set_session(self, sesison):
        self.session = sesison
