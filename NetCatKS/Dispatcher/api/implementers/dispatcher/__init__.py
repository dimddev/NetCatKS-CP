from twisted.internet.defer import Deferred

from zope.interface import implementer
from zope.component import adapts, subscribers
from zope.component import getGlobalSiteManager
from zope.interface.verify import verifyObject

from NetCatKS.Dispatcher.api.public import IDispatcher
from NetCatKS.Dispatcher.api.public import IDispathcherResultHelper

from NetCatKS.Components import IXMLResource
from NetCatKS.Components import IJSONResource, IJSONResourceAPI, IJSONResourceRootAPI

from NetCatKS.DProtocol.api.interfaces.subscribers import IJSONResourceSubscriber, IXMLResourceSubscriber

from NetCatKS.Validators.api.public import IValidator, ValidatorResponse

from NetCatKS.Logger import Logger

__author__ = 'dimd'


class NonRootAPI(object):

    def __init__(self, comp):

        self.comp = comp
        self.__logger = Logger()

    def check(self):

        for api in subscribers([self.comp], IJSONResourceAPI):

            if api.__class__.__name__.lower() in self.comp.to_dict().keys():

                self.__logger.debug('Candidate API {} for {}'.format(
                    api.__class__.__name__,
                    self.comp.__class__.__name__
                ))

                candidate_api_name = self.comp.to_dict().get(api.__class__.__name__.lower())

                try:
                    # execute the candidate API method
                    # and return the result
                    candidate_api_result = getattr(api, candidate_api_name)()

                except AttributeError as e:

                    msg = 'Candidate API {} for {} does not implement method {} error: {}'

                    self.__logger.warning(msg.format(
                        api.__class__.__name__,
                        self.comp.__class__.__name__,
                        candidate_api_name,
                        e.message
                    ))

                else:

                    self.__logger.info('Successful apply API {} for {}'.format(
                        api.__class__.__name__,
                        self.comp.__class__.__name__
                    ))

                    return candidate_api_result

        return False


class RootAPI(object):

    def __init__(self, comp):

        self.comp = comp
        self.__logger = Logger()

    def check(self):

        for api in subscribers([self.comp], IJSONResourceRootAPI):

            if api.__class__.__name__.lower() in self.comp.to_dict().keys():

                self.__logger.debug('Candidate API {} for {}'.format(
                    api.__class__.__name__,
                    self.comp.__class__.__name__
                ))

                self.__logger.info('Successful apply API {} for {}'.format(
                    api.__class__.__name__,
                    self.comp.__class__.__name__
                ))

                return api.process_factory()

        return False


@implementer(IDispatcher)
class Dispatcher(object):

    """
    Our Main dispatcher, Will trying to dispatch the request to API which provides functionality for it.
    The Dispatcher also adapts IValidator
    """

    adapts(IValidator)

    def __init__(self, validator):
        """

        :param validator:
        :type:

        """
        self.validator = validator
        self.__logger = Logger()

    def __api_processor(self, valid_dispatch, valid_response, isubscriber):
        """

        :param valid_dispatch:
        :param valid_response:
        :param isubscriber:
        :return:
        """
        for sub in subscribers([valid_response], isubscriber):

            self.__logger.debug('Matched request subscribers: {}'.format(sub.__class__.__name__))

            try:

                verifyObject(isubscriber, sub)

            except Exception as e:

                self.__logger.warning('Incorrect implementation: {}'.format(e))

            else:

                comp = sub.compare()

                if comp is not False and (IXMLResource.providedBy(comp) or IJSONResource.providedBy(comp)):

                    self.__logger.debug('Signature compare to {}'.format(comp.__class__.__name__))

                    # trying to resolve API that will deal with these request

                    if len(comp.to_dict().keys()) > 1:
                        # process request without root element
                        return NonRootAPI(comp).check()

                    else:
                        # root element
                        return RootAPI(comp).check()

        # if there are no one subsciber from IJSONResource

        self.__logger.warning('The request {} from type {} was not recognized as a structure or an API'.format(
            valid_response.response,
            valid_dispatch.message_type
        ))

        return False

    def dispatch(self):
        """
        When request is happening first will be validated,
        if valid_dispatch is False means we do not support this data type. You have to write your custom
        validator(s) inside components/validators
        Otherwise

        :return:
        """
        # validate for supporting types

        try:
            valid_dispatch = self.validator.validate()

        except Exception as e:

            self.__logger.debug('validate error: {}'.format(e.message))
            return self.validator

        else:

            if valid_dispatch is False:
                return self.validator

            valid_response = ValidatorResponse(valid_dispatch.message)

            if valid_dispatch.message_type == 'JSON':

                return self.__api_processor(
                    valid_dispatch,
                    valid_response,
                    IJSONResourceSubscriber
                )

            elif valid_dispatch.message_type == 'XML':

                return self.__api_processor(
                    valid_dispatch,
                    valid_response,
                    IXMLResourceSubscriber
                )


@implementer(IDispathcherResultHelper)
class DispathcherResultHelper(object):

    def __init__(self, factory):
        self.__logger = Logger()
        self.factory = factory

    def result_validation(self, sender=None, drop=None, section='TCP'):

        if IValidator.providedBy(self.factory):

            self.__logger.warning('{} Message is invalid: {}'.format(section, self.factory.message))

            if drop is not None:
                drop()

            else:
                return 'message is invalid'

        else:

            if self.factory:

                self.__logger.info('{} Response: {}'.format(section, self.factory))

                if IJSONResource.providedBy(self.factory):

                    if sender is not None:
                        sender(self.factory.to_json())

                    else:
                        return self.factory.to_json()

                elif IXMLResource.providedBy(self.factory):

                    if sender is not None:
                        sender(str(self.factory.to_xml()))

                    else:
                        return str(self.factory.to_xml())

                elif isinstance(self.factory, Deferred):

                    def deferred_response(response):

                        if sender is not None:
                            sender(response.to_json())

                    def deferred_response_error(err):

                        self.__logger.error('Cannot send message to user: {}'.format(
                            err
                        ))

                        return False

                    self.factory.addCallback(deferred_response)
                    self.factory.addErrback(deferred_response_error)

            else:

                self.__logger.warning('{}: This message was not be dispatched'.format(section))
                drop()

gsm = getGlobalSiteManager()
gsm.registerAdapter(Dispatcher)
