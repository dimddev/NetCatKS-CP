__author__ = 'dimd'


from zope.interface import Interface


class IDefaultLineReceiver(Interface):
    """
    The implementer has to provide functionality related for twisted LineReceiver
    """
