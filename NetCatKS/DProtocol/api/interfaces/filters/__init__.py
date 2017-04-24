__author__ = 'dimd'

from zope.interface import Interface


class IProtocolFiltersInterface(Interface):
    """
    Interface provides all needed checking condition, they are used when we want to have strictly types
    into our session field
    """
    def check_for_float_and_int(check):
        """
        This method have to provide condition to resolve that the input are integer or float
        :param check:
        :return: raise an TypeError if the input data is invalid otherwise True
        """

    def check_for_float(check):
        """
        This method have to provide condition to resolve that the input is float
        :param check:
        :return: raise an TypeError if the input data is invalid otherwise True
        """

    def check_for_int(check):
        """
        This method have to provide condition to resolve that the input is integer
        :param check:
        :return: raise an TypeError if the input data is invalid otherwise True
        """

    def check_for_list(check):
        """
        This method have to provide condition to resolve that the input is list
        :param check:
        :return: raise an TypeError if the input data is invalid otherwise True
        """

    def check_for_bool(check):
        """
        This method have to provide condition to resolve that the input is bool
        :param check:
        :return: raise an TypeError if the input data is invalid otherwise True
        """

    def check_for_dict(check):
        """
        This method have to provide condition to resolve that the input is dict
        :param check:
        :return: raise an TypeError if the input data is invalid otherwise True
        """

    def if_list_auto_append(in_data, add_to, max_len):

        """

        :param in_data: data to be adding to list
        :param add_to: add_to - list container

        :return: add_to
        :type: list
        """