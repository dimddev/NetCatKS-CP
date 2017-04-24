__author__ = 'dimd'


from zope.interface import Interface, Attribute


class IProtocolStogareInterface(Interface):

    """
    This interface define our session storage
    Every custom storage have to implement this Interface
    """

    session = Attribute(""" Container for our session """)