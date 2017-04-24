__author__ = 'dimd'

import imp
import os

from zope.interface import implementer
from zope.component import createObject
from zope.interface import implementedBy

from NetCatKS.Components.api.interfaces import IBaseLoader


@implementer(IBaseLoader)
class BaseLoader(object):

    def __init__(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        self.__storage = createObject('storageregister')

    def is_register(self, obj, filter_interfaces):

        try:

            is_reg = [
                (obj, candidate) for candidate in filter_interfaces if candidate in implementedBy(obj)
            ][-1]

        except IndexError:
            return False

        else:
            return is_reg

    def load(self, factories_source, filter_interface):

        """

        :param factories_source:
        :type factories_source: str

        :param filter_interface:
        :type filter_interface: list

        :return:
        """

        __klasses = []
        __ignore = ['DefaultAdapter']

        for root, subdirs, files in os.walk(factories_source):

            if files:

                for f in files:

                    if f.endswith('.pyc'):
                        continue

                    mod_path = root.replace('/', '.')

                    load = imp.load_source(mod_path, root + '/' + f)

                    for klass in dir(load):

                        try:

                            klass_obj = getattr(load, klass)
                            candidate = self.is_register(klass_obj, filter_interface)

                        except TypeError:
                            pass

                        else:

                            if candidate and klass not in __ignore:

                                __klasses.append(candidate)

                        if klass.startswith('I'):

                            if klass in __klasses or klass == 'Interface':
                                continue

                            self.__storage.interfaces[klass_obj.__name__.lower()] = {
                                'interface': klass_obj,
                                'origin_name': klass_obj.__name__
                            }

        return __klasses
