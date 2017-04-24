__author__ = 'dimd'

from NetCatKS.DProtocol.api.interfaces.filters import IProtocolFiltersInterface
from zope.interface import implementer


@implementer(IProtocolFiltersInterface)
class ProtocolFiltersImplementor(object):

    @staticmethod
    def check_for_float_and_int(check):

        """
        Implements `session.interface.filters.ISessionFiltersInterface.check_for_float_and_int
        :param check:
        :return:
        """

        if type(check) is not float and type(check) is not int:

            raise TypeError('API Error: incorrect configure, input must be float or int')

        else:
            return True

    @staticmethod
    def check_for_float(check):

        """

        :param check:
        :return:
        """

        if type(check) is not float:

            raise TypeError('API Error: incorrect configure, input must be float')

        else:
            return True

    @staticmethod
    def check_for_int(check):

        """

        :param check:
        :return:
        """
        if type(check) is not int:
            raise TypeError('API Error: incorrect configure, input must be int')

        else:
            return True

    @staticmethod
    def check_for_list(check):

        """

        :param check:
        :return:
        """
        if type(check) is not list:
            raise TypeError('API Error: incorrect configure, input must be list')

        else:
            return True


    @staticmethod
    def check_for_bool(check):

        """

        :param check:
        :return:
        """
        if type(check) is not bool:
            raise TypeError('API Error: incorrect configure, input must be bool')

        else:
            return True

    @staticmethod
    def check_for_dict(indict):

        """

        :param indict:
        :return:
        """

        if type(indict) is not dict:
            raise TypeError('API Error: incorrect congure, input must be dict')

        else:
            return True

    @staticmethod
    def if_list_auto_append(in_data, add_to, max_len=100000):
        """

        :param in_data: data to be adding to list
        :param add_to: add_to - list container

        :return: add_to
        :type: list
        """

        if type(add_to) is not list:
            raise TypeError('add_to must be a list')

        if in_data:

            if type(in_data) is list:
                # on update comes here
                if len(in_data) > max_len:
                    raise OverflowError('the len of a in_date is bigger than max_len')

                else:
                    add_to = in_data

            else:

                if in_data not in add_to:

                    if len(add_to) == max_len:
                        add_to.pop(0)

                    add_to.append(in_data)

            return add_to

        else:
            return add_to
