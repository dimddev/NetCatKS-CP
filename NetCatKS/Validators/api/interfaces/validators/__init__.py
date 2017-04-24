__author__ = 'dimd'

from zope.interface import Interface, Attribute


class IValidator(Interface):

    is_valid = Attribute('is this message valid')
    message_type = Attribute('show us the type of the message')

    def validate():
        """
        Validate incoming message for our supported types
        :return: self
        """


class IValidatorResponse(Interface):

    response = Attribute(
        """
        Helper interface that provides attribute to hold a valid response from our main validator
        """
    )

