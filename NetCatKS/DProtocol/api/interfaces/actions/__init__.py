__author__ = 'dimd'


from zope.interface import Interface, Attribute


class IBaseProtocolActionsInterface(Interface):
    """
    This interface defines all needed actions to works with our DynamicSession
    """
    def save():

        """
        Save current object into session storage, this method is a proxy to add_session,
        except self.id to be provided
        :return: True on success and raise Exception if self.id is not provided
        """

    def finish():
        """
        Session will be finished, this method will pop our session from session storage
        :return: False if self.id does not exist into our storage else self
        """

    def to_tdo(in_data):

        """

        :param in_data:
        :return:
        """

    def to_object(in_dict, in_obj):
        """
        One of the most used method of this API.
        It take care for converting input dict to object who is implement IBaseSessionActionsInterface
        and filling all object arguments with proper values.

        :param in_dict: Dict to be converted to object of kind IBaseSessionActionsInterface
        :param in_obj: This parameter is used only for our recursion and is not required during
        working with this method
        :return: self - the current object is updated with new values contained in in_dict

        """

    def to_dict(dob=None):

        """
        One of the most used method of this API. This method take care of converting of objects who are
        implemented IBaseSessionActionsInterface to dict

        :param dob: if obj is present, will create dict from it, otherwise will create dict from current object
        :return: dict
        """

    def to_json(**kwargs):
        """
        This methods convert objects from type IBaseSessionActionsInterface to JSON, the method have using
        self.to_dict() as proxy
        :return: IBaseSessionActionsInterface object as JSON
        """

    def get_session(**kwargs):
        """
        Trying to get our session by id from our session storage
        :param kwargs: id - required key
        :return: session on success - False otherwise
        """

    def add_session(**kwargs):
        """
        Adding of our session into our session storage
        :param kwargs: id and session - required keys
        :return:
        """

    def get_storage():
        """
        Return session storage
        :return: dict
        """

    def verify_storage(storage):
        """
        Will verify input candidate storage whether is a valid one, should implement ISessionStogareInterface
        :param storage:
        :return: storage or will raise exception
        """
    def flush_storage():
        """
        Flush session storage
        :return:
        """

    def public_setter(kwargs, service):
        """
        Take care of auto filling of all fileds of child object
        :param kwargs: dict of args (they must exist into child object)
        :param service: child obect
        :return: object
        """