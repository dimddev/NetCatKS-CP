__author__ = 'dimd'

from zope.interface import Interface, implementer


class IModeratorFactory(Interface):

    def delete_user(**kwargs):
        """
        delete user
        :param email:
        :return:
        """


@implementer(IModeratorFactory)
class ModeratorFactory(object):

    def delete_user(self, **kwargs):
        print 'DELETE USER WITH EMAIL {}'.format(kwargs.get('email'))