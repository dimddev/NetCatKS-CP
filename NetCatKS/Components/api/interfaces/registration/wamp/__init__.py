__author__ = 'dimd'


from zope.interface import Interface, Attribute


class IRegisterWamp(Interface):

    def register():
        """
        Registering of all objects which ends with Wamp prefix and are located inside component/wamp directory
        :return:
        """


class IWAMPResource(Interface):
    """
    marker
    """


class IWAMPComponent(Interface):

    def set_session(session):
        """
        register session to self.session
        :param session: Wamp Session
        :return:
        """


class IWAMPLoadOnRunTime(Interface):
    """
    marker for API's that have to be run, after we join in WAMP session
    """

    def load():
        """
        trying to load on runtime some wamp RPC
        :return: IJSONResource
        """