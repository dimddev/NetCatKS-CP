__author__ = 'dimd'

from zope.interface import alsoProvides
from NetCatKS.Components.api.interfaces.virtual import IVirtualAdapter


class AdapterProxyGetter(object):
    """
    This class overwrites __getattr__ magic method and provides a easy way to deal
    with multiadapters ( combine many object into one) we will walking through all adaptee
    object and will trying to find to where belong, the will be returned so we play here with
    ProxyGetter
    """
    __debug = False

    def __init__(self, *args):

        self._adapters = args

        super(AdapterProxyGetter, self).__init__()

    def __getattr__(self, name):
        """
        returning matched attribute or method otherwise raise AttributeError
        :param name: list of adaptee objects
        :return: matched attribute or method or raise AttributeError
        """

        checker = []

        for obj in self._adapters:

            try:

                # for normal attributes
                if obj.__dict__.get(name, None) is not None:

                    return obj.__dict__.get(name)

                # for properties
                elif getattr(obj, name) and not callable(getattr(obj, name)):
                    return getattr(obj, name)

                # for methods
                elif callable(getattr(obj, name)):

                    def proxy(*args, **kwargs):
                        setattr(self, obj.__class__.__name__.lower(), obj)
                        return getattr(obj, name)(*args, **kwargs)

                    return proxy

            except Exception as e:
                checker.append(1)

                if AdapterProxyGetter.__debug is True:
                    print 'DEBUG EXCEPTION: {}'.format(e.message)

                else:
                    pass

        if len(checker) == len(self._adapters):

            error = type(
                'InvalidAttribute',
                (object,),
                {
                    'message': 'attribute {} does not exist'.format(name),
                    'error': True,
                    name: False
                }
            )

            alsoProvides(error, IVirtualAdapter)
            return error()

__all__ = [
    'AdapterProxyGetter'
]
