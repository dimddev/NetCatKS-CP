from NetCatKS.Components.api.implementers.default import DefaultAdapter
from NetCatKS.Components.api.interfaces.adapters import IDynamicAdapterFactory, IRequestSubscriber

from zope.component import adapter, createObject, adapts
from zope.component import getGlobalSiteManager
from zope.interface import implementer

from NetCatKS.Components.api.interfaces.adapters import IJSONResourceRootAPI, IJSONResourceAPI
from NetCatKS.Components.api.interfaces.loaders import IJSONResource
from NetCatKS.Components.api.interfaces.registration.wamp import IWAMPLoadOnRunTime

__author__ = 'dimd'


class _WampSessionProvider(object):

    def get_session(self):

        return createObject('storageregister').components.get(
            '__wamp_session__', False
        )


@implementer(IJSONResourceAPI)
class BaseAPI(object):

    adapts(IJSONResource)

    def __init__(self, factory):
        self.factory = factory


@implementer(IJSONResourceRootAPI)
class BaseRootAPI(object):

    adapts(IJSONResource)

    def __init__(self, factory):
        self.factory = factory

    def process_factory(self):
        raise NotImplemented


class BaseAPIWampMixin(BaseAPI, _WampSessionProvider):
    def __init__(self, factory):
        super(BaseAPIWampMixin, self).__init__(factory)


class BaseRootAPIWampMixin(BaseRootAPI, _WampSessionProvider):

    def __init__(self, factory):
        super(BaseRootAPIWampMixin, self).__init__(factory)


@implementer(IWAMPLoadOnRunTime)
class WAMPLoadOnRunTime(_WampSessionProvider):

    adapts(IJSONResource)

    def __init__(self, factory):
        self.factory = factory

    def load(self):
        raise NotImplemented('User must implement this method')


@implementer(IRequestSubscriber)
class RequestSubscriber(object):

    def subscribe_me(self):
        return True


@implementer(IDynamicAdapterFactory)
class DynamicAdapterFactory(object):

    def __init__(self, *args, **kwargs):

        super(DynamicAdapterFactory, self).__init__()

        args = args[0]

        klass = adapter(*args)

        self.__klass = klass(
            type(
                kwargs.get('name', 'DynamicAdapter'),
                (DefaultAdapter, ),
                {}
            )
        )

        gsm = getGlobalSiteManager()
        gsm.registerAdapter(self.__klass)

    def get(self):
        return self.__klass