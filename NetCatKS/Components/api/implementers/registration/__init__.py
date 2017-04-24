__author__ = 'dimd'

from zope.component import createObject
from zope.interface.interfaces import ComponentLookupError
from NetCatKS.Config.api.implementers import Config


class ComponentsRegistratorAdapter(object):

    """
    Adapt together RegisterFactories and RegisterAdapters
    """

    def __init__(self, *args, **kwargs):

        """
        :param want_to_load:
        :type want_to_load: list

        :param kwargs: adapters_source, factories_source, sessions_source, utility_source

        :return:
        """

        super(ComponentsRegistratorAdapter, self).__init__()

        self.__available_components = [
            'adapters', 'factories',
            'protocols', 'utility',
            'validators', 'wamp'
        ]

        self.config = Config()
        self.adapters_source = kwargs.get('adapters_source', 'components/adapters')
        self.factories_source = kwargs.get('factories_source', 'components/factories')
        self.protocols_source = kwargs.get('protocols_source', 'components/protocols')
        self.utility_source = kwargs.get('utility_source', 'components/utility')
        self.validators_source = kwargs.get('validators_source', 'components/validators')
        self.wamp_source = kwargs.get('wamp_source', 'components/wamp')

        __a_comp = kwargs.get('components', None)

        comp = []

        if __a_comp is not None and type(__a_comp) is list:

            comp = [c for c in __a_comp if c in self.__available_components]

            if not comp:

                raise AttributeError('Incorrect attribute an available are: {}'.format(
                    ', '.join(self.__available_components)
                ))

        self.running_components = comp or self.__available_components

    def init(self):
        
        for reg in self.running_components:

            try:

                source = getattr(self, '{}_source'.format(reg))

                reg_component = createObject('register{}'.format(reg), source)

            except AttributeError as e:
                print e.message
                pass

            except TypeError as e:

                print e.message, 'register{}'.format(reg)
                return

            except ComponentLookupError:
                pass

            else:

                reg_component.register()

        return self


class ComponentsRegistration(ComponentsRegistratorAdapter):
    """

    """
    def __init__(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return:
        """
        super(ComponentsRegistration, self).__init__(*args, **kwargs)


__all__ = [
    'ComponentsRegistration',
    'ComponentsRegistratorAdapter'
]