__author__ = 'dimd'

from NetCatKS.Components.api.interfaces.registration.protocols import IRegisterProtocols
from NetCatKS.Components.api.implementers.registration.factories import RegisterFactories
from NetCatKS.Components.api.interfaces import IJSONResource

from zope.interface import implementer
from zope.component import getGlobalSiteManager
from zope.component.factory import Factory
from zope.component.interfaces import IFactory


@implementer(IRegisterProtocols)
class RegisterProtocols(RegisterFactories):

    def __init__(self, protocols_source, file_loader=None, out_filter=list()):

        default_filters = list(set(out_filter + [IJSONResource]))
        super(RegisterProtocols, self).__init__(protocols_source, file_loader, default_filters)


gsm = getGlobalSiteManager()

factory_ = Factory(RegisterProtocols, RegisterProtocols.__name__)
gsm.registerUtility(factory_, IFactory, RegisterProtocols.__name__.lower())