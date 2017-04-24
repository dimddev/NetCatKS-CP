__author__ = 'dimd'

from zope.interface import Interface, Attribute, implementer


class IUserFactory(Interface):

    is_logged = Attribute("is user logged in")

    def register(username, validator, **kwargs):
        """
        Registering new user
        :param username:
        :param email:
        :param password:
        :return:
        """

    def login(email, **kwargs):
        """
        Loggin into the system
        :param email:
        :param password:
        :return:
        """

    def logout():
        """
        logout from the system
        :return:
        """

    def send_coordinates(**kwargs):
        """
        sending gps coordinates
        :param long:
        :param lat:
        :return:
        """


@implementer(IUserFactory)
class UserFactory(object):

    def __init__(self):
        self.__is_user = True

    @property
    def is_user(self):
        return self.__is_user

    def register(self, **kwargs):

        print 'USER {} WAS REGISTERED WITH EMAIL {} AND PASSWORD {}'.format(
            kwargs.get('username'), kwargs.get('email'), kwargs.get('password')
        )

    def login(self, **kwargs):

        print 'USER WITH EMAIL {} AND PASSWORD {} IS LOGGED IN.'.format(
            kwargs.get('email'), kwargs.get('password')
        )

    def logout(self):

        print 'USER LOGGED OUT...'

    def send_coordinates(self, **kwargs):

        print 'USER LONG {} LAT {}'.format(kwargs.get('long'), kwargs.get('lat'))