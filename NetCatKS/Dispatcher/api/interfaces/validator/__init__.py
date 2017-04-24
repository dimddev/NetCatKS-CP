__author__ = 'dimd'

from zope.interface import Interface


class IDispatchAPIValidator(Interface):

    def validate(check_one, check_two):

        """
        validate whether in_dict.keys.sort() is equal to self.to_dict().keys().sort()
        :param in_dict: dict
        :return: bool
        """
