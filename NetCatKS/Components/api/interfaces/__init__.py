from NetCatKS.Components.api.interfaces.adapters import IDynamicAdapterFactory, IXMLResourceAPI
from NetCatKS.Components.api.interfaces.adapters import IJSONResourceAPI, IJSONResourceRootAPI, IRequestSubscriber
from NetCatKS.Components.api.interfaces.loaders import IBaseLoader, IXMLResource
from NetCatKS.Components.api.interfaces.registration.adapters import IRegisterAdapters
from NetCatKS.Components.api.interfaces.registration.factories import IRegisterFactories
from NetCatKS.Components.api.interfaces.registration.protocols import IRegisterProtocols
from NetCatKS.Components.api.interfaces.registration.wamp import IWAMPResource, IRegisterWamp, IWAMPComponent
from NetCatKS.Components.api.interfaces.registration.wamp import IWAMPLoadOnRunTime

from NetCatKS.Components.api.interfaces.storages import IStorageRegister
from NetCatKS.Components.api.interfaces.loaders import IUserFactory, IUserStorage, IUserWampComponent
from NetCatKS.Components.api.interfaces.loaders import IUserGlobalSubscriber, IJSONResource

__author__ = 'dimd'

__all__ = [
    'IDynamicAdapterFactory',
    'IBaseLoader',
    'IRegisterAdapters',
    'IRegisterFactories',
    'IRegisterProtocols',
    'IStorageRegister',
    'IWAMPResource',
    'IRegisterWamp',
    'IWAMPComponent',
    'IUserFactory',
    'IUserStorage',
    'IUserWampComponent',
    'IUserGlobalSubscriber',
    'IJSONResource',
    'IJSONResourceAPI',
    'IJSONResourceRootAPI',
    'IRequestSubscriber',
    'IXMLResourceAPI',
    'IXMLResource',
    'IWAMPLoadOnRunTime'
]