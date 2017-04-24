__author__ = 'dimd'

from NetCatKS.DProtocol.api.implementors.actions import BaseProtocolActionsImplementor


class BaseProtocolActions(BaseProtocolActionsImplementor):
    def __init__(self, **kwargs):
        super(BaseProtocolActions, self).__init__(**kwargs)