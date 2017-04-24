__author__ = 'dimd'

from zope.interface import Interface, Attribute


class IDynamicProtocolInterface(Interface):

    """
    This interface will assign to every protocol required id filed, this filed is used
    for unique identity and also all method which play with our session will looking for it
    """

    id = Attribute(""" id for our session """)
