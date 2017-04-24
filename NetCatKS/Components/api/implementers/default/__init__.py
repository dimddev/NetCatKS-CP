__author__ = 'dimd'

from ...interfaces.virtual import IVirtualAdapter
from ....common.adapters import AdapterProxyGetter

from zope.interface import implementer


@implementer(IVirtualAdapter)
class DefaultAdapter(AdapterProxyGetter):

    def __init__(self, *args):
        super(DefaultAdapter, self).__init__(*args)
