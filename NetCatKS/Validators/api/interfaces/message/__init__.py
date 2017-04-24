__author__ = 'dimd'


from zope.interface import Interface, Attribute


class IMessage(Interface):
    """
    Interface which provide a message attribute, representing incoming message.
    The message usually is the data who arrived to us from some where
    """
    message = Attribute("Represent incoming message")
