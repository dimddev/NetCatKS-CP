from __future__ import absolute_import

from NetCatKS.Components.api.interfaces.registration.wamp import IRegisterWamp
from NetCatKS.Components.common.loaders import BaseLoader
from NetCatKS.Components.api.interfaces import IUserWampComponent, IUserGlobalSubscriber, IWAMPComponent
from zope.component.factory import Factory
from zope.component.interfaces import IFactory

from zope.interface import implementer
from zope.component import getGlobalSiteManager

from datetime import datetime

__author__ = 'dimd'


@implementer(IRegisterWamp)
class RegisterWamp(object):

    """
    Take care for registration of all wamp components
    """

    def __init__(self, wamp_source, file_loader=None, out_filter=None):
        """

        :param file_loader:
        :param wamp_source:
        :return:
        """

        self.__gsm = getGlobalSiteManager()
        self.file_loader = file_loader or FileWampLoader()

        self.default_filter = out_filter or [IUserWampComponent, IUserGlobalSubscriber, IWAMPComponent]

        self.__objects = self.file_loader.load(
            wamp_source, self.default_filter

        )

        super(RegisterWamp, self).__init__()

    def register(self):
        """

        :return:
        """
        if type(self.__objects) is not tuple and type(self.__objects) is not list:
            raise TypeError('objects have to be tuple or list')

        __ignore_list = [
            'BaseWampComponent'
        ]

        for obj, obj_interface in self.__objects:

            if obj.__name__ in __ignore_list:
                continue

            print('{} [ RegisterWamp ] Loading Wamp Component: {}, filter interface: {}'.format(
                datetime.now(), obj.__name__, obj_interface.__name__
            ))

            self.__gsm.registerSubscriptionAdapter(obj)


class FileWampLoader(BaseLoader):

    def __init__(self, **kwargs):
        """
        Load all classes ending with kwargs['prefix'] eg. 'Wamp', default is 'Adapter"
        :param kwargs:
        :return:
        """
        super(FileWampLoader, self).__init__(**kwargs)


gsm = getGlobalSiteManager()

factory_ = Factory(RegisterWamp, RegisterWamp.__name__)
gsm.registerUtility(factory_, IFactory, RegisterWamp.__name__.lower())