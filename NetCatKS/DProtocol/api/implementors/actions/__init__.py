__author__ = 'dimd'

import json
import xmltodict

from zope.interface import implementer
from zope.interface.exceptions import DoesNotImplement


from NetCatKS.DProtocol.api.interfaces.actions import IBaseProtocolActionsInterface
from NetCatKS.DProtocol.api.interfaces.storage import IProtocolStogareInterface
from NetCatKS.DProtocol.api.public.storage import ProtocolStorage
from NetCatKS.DProtocol.api.implementors.filters import ProtocolFiltersImplementor


@implementer(IBaseProtocolActionsInterface)
class BaseProtocolActionsImplementor(ProtocolFiltersImplementor):

    """
    This class provides implementation of `session.interfaces.actions.IBaseSessionActionsInterface`
    """

    def __init__(self, **kwargs):
        """

        :param kwargs:
        :return: None
        """
        storage = kwargs.get('storage', None)

        if storage is not None:
            self.__storage = self.verify_storage(storage)

        else:
            self.__storage = self.verify_storage(ProtocolStorage())

        super(BaseProtocolActionsImplementor, self).__init__()

    def to_tdo(self, in_data):

        def inner(apidata, indata):
            """

            :param apidata:
            :type apidata: dprotocol instance
            :param indata:
            :type indata: iterable
            :param deep: how deep I'm

            :return: dict
            """

            # apidata is a dprotocol instance, predefined inside our backend as
            # DProtocol implementation in both way it inherit from BaseProtocolActions which provides
            # IBaseProtocolActionsInterface

            for k, v in apidata.to_dict().iteritems():

                # so if we meet attribute from IBaseProtocolActionsInterface type means it's a sub protocol
                # and we have to call inner
                if IBaseProtocolActionsInterface.providedBy(getattr(apidata, k)):
                    inner(getattr(apidata, k), indata)

                else:

                    # otherwise we will looping over all items in indata
                    for ik, iv in indata.iteritems():

                        # 1. we checking whether the ik exist directly in our root dict of apidata
                        if ik in apidata.to_dict():

                            # if exist we get the value from apidata.to_dict().get(ik) with ik as key
                            indata[ik] = apidata.to_dict().get(ik)

                        elif type(iv) is dict:

                            # 2.if iv is a dict first we will trying to get the k apidata key
                            # from this dict

                            if k in iv:

                                # if exist will update the indata for this key
                                indata[ik].update({k: apidata.to_dict().get(k)})

                            else:

                                # else we pass the iv to our inner again for more
                                # nested structures
                                inner(apidata, iv)
            return indata

        result = inner(self, in_data)

        return result

    def save(self):
        """

        :return:
        """

        try:

            if self.id is None:

                raise ValueError('The session id is not assigned')

        except AttributeError:

            raise NotImplementedError('the storage methods works only with protocols which provide a id attribute')

        self.add_session(id=self.id, session=self)
        return True

    def finish(self):

        """

        :return:
        """
        return False if not self.__storage.session.pop(self.id, False) else self

    def to_object(self, in_dict=None, in_obj=None):

        """

        :param in_dict:
        :param in_obj:
        :return:
        """

        if in_dict is None:
            return False

        if in_obj is not None:
            self = in_obj

        def get_child(child_members, in_dict):

            child_object = getattr(self, child_members)

            if not isinstance(child_object, BaseProtocolActionsImplementor):
                setattr(self, child_members, in_dict[child_members])

            else:

                self.to_object(
                    in_dict=in_dict.get(child_members),
                    in_obj=child_object
                )

        for members, members_value in in_dict.iteritems():

            if type(members_value) is dict or isinstance(members_value, BaseProtocolActionsImplementor):

                get_child(members, in_dict)

            else:

                if members == '_BaseProtocolActionsImplementor__storage':
                    continue

                setattr(self, members, members_value)

        return self

    def nice_name(self, in_name):

        # if not in_name.startswith('__'):
        #    raise AttributeError('attribute {} is not defined as private'.format(in_name))

        temp, result = in_name.rsplit('__')
        return result

    def to_dict(self, dob=None):

        """

        :param dob:
        :return:
        """

        temp = {}

        if dob is not None:
            self = dob

        for members in self.__dict__:

            if members == '_BaseProtocolActionsImplementor__storage':
                continue

            if isinstance(self.__dict__[members], BaseProtocolActionsImplementor) is True:
                temp[self.nice_name(members)] = self.to_dict(dob=self.__dict__[members])

            else:

                # here we cover a case when we have a list and inside this list
                # we have members from IBaseProtocolActionsInterface
                # and convert all members to dict
                # this is not usual case and to_object will not work

                if isinstance(self.__dict__[members], list):
                    tmp = []

                    for mem in self.__dict__[members]:

                        if isinstance(mem, BaseProtocolActionsImplementor) is True:
                            tmp.append(mem.to_dict())

                    if tmp:
                        temp[self.nice_name(members)] = tmp

                    else:
                        temp[self.nice_name(members)] = self.__dict__[members]

                else:
                    temp[self.nice_name(members)] = self.__dict__[members]

        return temp

    def to_json(self, **kwargs):
        """

        :param indent:
        :return:
        """
        indent = kwargs.get('indent', None)

        if indent is not None and type(indent) is int:
            return json.dumps(self.to_dict(), indent=indent)

        else:
            return json.dumps(self.to_dict())

    def to_xml(self, in_dict=None):

        """

        Convert dict to xml

        :param in_dict:

        :return: xml
        """

        try:

            xml = xmltodict.unparse(in_dict or self.to_dict())

        except ValueError as e:
            raise ValueError(e.message)

        else:
            return xml

    def get_session(self, **kwargs):

        """

        :param kwargs:
        :return:
        """

        if 'id' in kwargs and kwargs.get('id'):
            return self.__storage.session.pop(kwargs.get('id'), False)

        else:
            raise AttributeError('Incorrect configure, the id is a required argument')

    def add_session(self, **kwargs):
        """

        :param kwargs:
        :return:
        """

        if 'id' in kwargs and 'session' in kwargs:

            _id = kwargs.get('id')

            if _id in self.__storage.session:
                return False

            session = kwargs.get('session')

            if not isinstance(session, BaseProtocolActionsImplementor) is True:
                raise AttributeError('Incorrect configure, you must pass a DProtocol implementation as session argument')

            self.__storage.session[_id] = session

            return self

        else:
            raise AttributeError('Incorrect configure, the id and a session are required arguments')

    def get_storage(self):

        """

        :return:
        """
        return self.__storage.session

    def flush_storage(self):

        """

        :return:
        """
        self.__storage.session = {}

    def verify_storage(self, storage):

        """

        :param storage:
        :return:
        """
        if not IProtocolStogareInterface.providedBy(storage):

            raise DoesNotImplement(
                'A storage {} does not implement IProtocolStogareInterface'.format(storage)
            )

        else:
            return storage

    @staticmethod
    def public_setter(kwargs, service):
        """

        :param kwargs:
        :param service:
        :return:
        """
        # get all attributes
        keys = kwargs.keys()

        # loop over them
        for k in keys:

            search_key = '_{}__{}'.format(service.__class__.__name__, k)

            # if these attribute are into this service dict
            if search_key in service.__dict__:
                # set it
                setattr(service, k, kwargs[k])

            else:
                raise AttributeError('Incorrect configure for {}, key: {}'.format(service, k))

        # if user are passed correct service attributes, they are set
        # otherwise just return requested service without changes
        return service

    # original from http://www.saltycrane.com/blog/2011/10/some-more-python-recursion-examples/
    # modified by dimd
    def get_all_keys(self, data=None):

        """
        This function gets all keys from dict recursively
        :param data:
        :type data: dict

        :return: list of keys
        """

        data = data or self.to_dict()

        keys = []

        def inner(data):

            if isinstance(data, dict):

                for k, v in data.iteritems():
                    if (isinstance(v, dict) or
                        isinstance(v, list) or
                        isinstance(v, tuple)
                        ):
                        keys.append(k)
                        inner(v)
                    else:
                        keys.append(k)

            elif isinstance(data, list) or isinstance(data, tuple):
                for item in data:
                    inner(item)

        inner(data)
        return keys