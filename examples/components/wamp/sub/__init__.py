from NetCatKS.Components import IUserGlobalSubscriber, IJSONResource

from zope.interface import implementer
from zope.component import adapts


@implementer(IUserGlobalSubscriber)
class GlobalSubscriberCallBackWamp(object):

    adapts(IJSONResource)

    def __init__(self, adapt=None):
        self.adapt = adapt

    def subscribe(self):
        print self.adapt.to_dict()

