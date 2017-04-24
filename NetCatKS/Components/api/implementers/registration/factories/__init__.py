from __future__ import absolute_import

__author__ = 'dimd'

from datetime import datetime

from zope.interface import implementer
from zope.component import createObject
from zope.component import getGlobalSiteManager
from zope.component.factory import Factory
from zope.component.interfaces import IFactory

from NetCatKS.Components.api.interfaces.registration.factories import IRegisterFactories
from NetCatKS.Components.common.loaders import BaseLoader
from NetCatKS.Components.api.interfaces import IUserStorage, IUserFactory
from NetCatKS.Validators import IValidatorResponse
from NetCatKS.DProtocol import DProtocolSubscriber
from NetCatKS.Logger import Logger
from NetCatKS.Components.api.interfaces import IJSONResource


@implementer(IRegisterFactories)
class RegisterFactories(object):

    def __init__(self, factories_source, file_loader=None, out_filter=list()):
        """

        :param file_loader:
        :param factories_source:
        :return:
        """

        super(RegisterFactories, self).__init__()

        self.__gsm = getGlobalSiteManager()

        self.file_loader = file_loader or FileFactoryLoader()

        self.default_filter = list(set(out_filter + [IUserStorage, IUserFactory]))

        self.__objects = self.file_loader.load(
            factories_source, self.default_filter

        )

        self.__storage = createObject('storageregister')
        self.__logger = Logger()

    def get_object(self):
        return self.__objects

    def register(self):
        """

        :return:
        """
        if type(self.__objects) is not tuple and type(self.__objects) is not list:
            raise TypeError('objects have to be tuple or list')

        self.__objects = set(self.__objects)

        for obj, obj_interface in self.__objects:

            __ignore = ['Factory', 'IFactory']

            if obj.__name__ in __ignore:
                continue

            print('{} [ RegisterFactories ] Load: {} with filter: {}'.format(
                str(datetime.now()), obj.__name__,
                obj_interface.__name__
            ))

            if obj_interface is IJSONResource:

                try:

                    subscribe_me = getattr(obj(), 'subscribe_me')()

                except AttributeError:
                    pass

                else:

                    def __init(self, adapter):
                        self.adapter = adapter

                    if subscribe_me is True:

                        __klass = type(
                            'DynamicAdapter{}'.format(obj.__name__),
                            (DProtocolSubscriber, ),
                            {'__init__': __init, 'protocol': None}
                        )

                        setattr(__klass, 'protocol', obj())
                        self.__gsm.registerSubscriptionAdapter(__klass, [IValidatorResponse])

            # NETODO to be checked and removed is needed
            # reg_name = obj.__name__.lower().replace(self.file_loader.prefix.lower(), '')
            # self.__storage.components[reg_name] = self.file_loader.prefix.lower()

            factory = Factory(obj, obj.__name__)
            self.__gsm.registerUtility(factory, IFactory, obj.__name__.lower())


class FileFactoryLoader(BaseLoader):

    def __init__(self, **kwargs):
        """
        Load all classes ending with kwargs['prefix'] default is 'Factory"
        :param kwargs:
        :return:
        """
        super(FileFactoryLoader, self).__init__(**kwargs)


gsm = getGlobalSiteManager()

factory_ = Factory(RegisterFactories, RegisterFactories.__name__)
gsm.registerUtility(factory_, IFactory, RegisterFactories.__name__.lower())