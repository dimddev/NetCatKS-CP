__author__ = 'dimd'

import xmltodict
import json

from zope.component import adapts
from zope.interface import implementer, classImplementsOnly

from NetCatKS.DProtocol.api.interfaces.subscribers import IBaseResourceSubscriber, IJSONResourceSubscriber
from NetCatKS.DProtocol.api.interfaces.subscribers import IXMLResourceSubscriber
from NetCatKS.Validators import IValidatorResponse
from NetCatKS.Logger import Logger


@implementer(IBaseResourceSubscriber)
class BaseProtocolSubscriber(object):

    def __init__(self, adapter):
        """

        :param adapter IJSONResource
        """

        try:

            getattr(self, 'protocol')

        except AttributeError:
            raise AttributeError('Wrong implementation, you must subclass the protocol attribute')

        else:

            self.adapter = adapter

        super(BaseProtocolSubscriber, self).__init__()

    def compare_debug(self, level, in_dict, host_proto):

        logger = Logger()
        logger.debug('COMPARE LEVEL {}'.format(level))
        logger.debug('IN_DICT: {}'.format(in_dict))
        logger.debug('HOST_PROTO: {}'.format(host_proto))
        logger.debug('END COMPARE LEVEL {}'.format(level))

    def compare(self):

        # xml

        if type(self.adapter) is tuple:

            try:
                self.adapter = self.adapter[0]

            except IndexError as e:

                print e.message
                pass

        if type(self.adapter.response) is str:

            try:

                self.adapter.response = xmltodict.parse(self.adapter.response)

                # this dirty trick will make convert OrderedDict to normal
                # because our DProtocol API currently does not support OrderDict
                # when we starting to support XML with name spaces have to be extended

                self.adapter.response = json.dumps(self.adapter.response)
                self.adapter.response = json.loads(self.adapter.response)

            except Exception as e:
                print e.message

        # normal case

        self.protocol.__init__()

        in_dict = self.protocol.get_all_keys(self.adapter.response)
        host_proto = self.protocol.get_all_keys(self.protocol.to_dict())

        in_dict.sort()
        host_proto.sort()

        # self.compare_debug(1, in_dict, host_proto)

        if ''.join(in_dict) == ''.join(host_proto):
            return self.protocol.to_object(self.adapter.response)

        else:

            in_dict = self.adapter.response.keys()
            host_proto = self.protocol.to_dict().keys()

            in_dict.sort()
            host_proto.sort()

            # self.compare_debug(2, in_dict, host_proto)

            if ''.join(in_dict) == ''.join(host_proto):
                return self.protocol.to_object(self.adapter.response)

            return False


class DProtocolSubscriber(BaseProtocolSubscriber):

    """
    This class is designed to be subclassed not for directly usage
    """

    adapts(IValidatorResponse)

    def __init__(self, adapter):
        """
        :param adapter IJSONResource
        """
        super(DProtocolSubscriber, self).__init__(adapter)


classImplementsOnly(DProtocolSubscriber, IJSONResourceSubscriber)


class DProtocolXMLSubscriber(BaseProtocolSubscriber):

    adapts(IValidatorResponse)

    def __init__(self, adapter):
        super(DProtocolXMLSubscriber, self).__init__(adapter)

classImplementsOnly(DProtocolXMLSubscriber, IXMLResourceSubscriber)


