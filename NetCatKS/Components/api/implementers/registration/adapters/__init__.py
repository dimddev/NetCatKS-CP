__author__ = 'dimd'

from datetime import datetime

from NetCatKS.Components.api.interfaces.virtual import IVirtualAdapter
from NetCatKS.Components.api.interfaces.registration.adapters import IRegisterAdapters
from NetCatKS.Components.api.implementers.adapters import DynamicAdapterFactory
from NetCatKS.Components.api.implementers.registration.factories import RegisterFactories
from NetCatKS.Components.api.interfaces import IJSONResourceAPI, IJSONResourceRootAPI, IWAMPLoadOnRunTime

from NetCatKS.Components.common.loaders import BaseLoader
from NetCatKS.Components.common.factory import get_factory_objects

from zope.component import getMultiAdapter
from zope.component import ComponentLookupError
from zope.component import getGlobalSiteManager, createObject
from zope.interface import implementer
from zope.component.factory import Factory
from zope.component.interfaces import IFactory


@implementer(IRegisterAdapters)
class RegisterAdapters(RegisterFactories):
    """
    This class provide functionality for registering adapters inside Zope Global Site Manager
     ( storage of kind )
    """
    def __init__(self, protocols_source, file_loader=None, out_filter=list()):
        """

        :param protocols_source:

        :param file_loader:

        :param out_filter:

        :return:
        """
        default_filters = list(
            set(out_filter + [IVirtualAdapter, IJSONResourceAPI, IJSONResourceRootAPI, IWAMPLoadOnRunTime])
        )

        super(RegisterAdapters, self).__init__(protocols_source, file_loader, default_filters)

        self.__storage = createObject('storageregister')

        self.__objects = self.get_object()

        self.__gsm = getGlobalSiteManager()

    def register(self):
        """

        :return:
        """

        if type(self.__objects) is not tuple and type(self.__objects) is not list:
            raise TypeError('objects have to be tuple or list')

        self.__objects = list(set(self.__objects))

        __skip_system_helpers = [
            'BaseAPI', 'BaseRootAPI', 'BaseRootAPIWampMixin', 'BaseAPIWampMixin', 'WAMPLoadOnRunTime'
        ]

        for adapter, adapter_interface in self.__objects:

            if adapter.__name__.startswith('I') or adapter.__name__ in __skip_system_helpers:
                continue

            print('{} [ RegisterAdapters ] Load: {} with filter: {}'.format(
                str(datetime.now()), adapter.__name__,
                adapter_interface.__name__
            ))

            self.__gsm.registerSubscriptionAdapter(adapter)

        return True

    def get_multi_adapter(self, objects, belong_interface=IVirtualAdapter):
        """
        This function will return proper multi adapter
        :param objects: list of objects like ['user', 'admin']
        :param belong_interface: default is IVirtualAdapter
        :return: adapted object
        """

        # first we trying to get multi adapters based on all registered factories
        try:

            if type(objects) is not tuple and type(objects) is not list:
                raise TypeError('objects have to be tuple or list')

            return getMultiAdapter(get_factory_objects(objects), belong_interface)

        except ComponentLookupError:

            iface_collection = []

            for obj in objects:

                iface_name = 'i{}{}'.format(obj, self.__storage.components.get(obj))
                iface = self.__storage.interfaces.get(iface_name, None)

                if iface:
                    iface_collection.append(iface.get('interface'))

            # will trying to make dynamic adapter based on current request

            DynamicAdapterFactory(iface_collection)
            return getMultiAdapter(get_factory_objects(objects), belong_interface)


class FileAdaptersLoader(BaseLoader):

    def __init__(self, **kwargs):
        """
        Load all classes
        :param kwargs:
        :return:
        """
        super(FileAdaptersLoader, self).__init__(**kwargs)


gsm = getGlobalSiteManager()

factory_ = Factory(RegisterAdapters, RegisterAdapters.__name__)
gsm.registerUtility(factory_, IFactory, RegisterAdapters.__name__.lower())