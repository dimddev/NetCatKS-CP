__author__ = 'dimd'

from zope.interface import Interface, implementer


class IAdminFactory(Interface):

    def delete_moderator(**kwargs):
        """
        """

@implementer(IAdminFactory)
class AdminFactory(object):

    def __init__(self):
        self.__is_admin = True

    @property
    def is_admin(self):
        return self.__is_admin

    def delete_moderator(self, **kwargs):

        print 'ADMIN DELETE MODERATOR: EMAIL: {} USERNAME: {}'.format(
            kwargs.get('email'), kwargs.get('username')
        )