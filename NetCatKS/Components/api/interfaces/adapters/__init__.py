__author__ = 'dimd'

from zope.interface import Interface, Attribute


class IRequestSubscriber(Interface):

    def subscribe_me():
        """
        Attribute that mark protocol as structure that care about request
        :return: True
        """


class IDynamicAdapterFactory(Interface):

    def get():
        """
        return new dynamic adapter prepared by __init__
        :return: class
        """


class IJSONResourceRootAPI(Interface):

    """
    Marker for API's which adapts IJSONResource

    All API's from this type have to be stored inside components/adapters
    directory. They will be loaded on runtime by NetCatKS and will be registered
    as SubscriptionAdapter inside zope global site manager.

    Later, when request arriving the Dispatcher will deal with all adapter API's which are registered
    as IJSONResourceRootAPI implementer

    The implementer of this interface have to provide a functionality
    that deal with structures defined by DProtocol API. By default all
    of them is expected to by from type IJSONResource.

    The implementer have to use zope.interface.implementer to mark
    an API as resource from type IJSONResourceAPI and zope.compoment.adapts
    for an adapting an IJSONResource

    The API from type IJSONResourceAPI must provide functionality that deals
    with root based structures, which meaning we have one root element and
    inside it our custom structures or:

    {"time_operation":
        {
            "location" : {
                "longitude": 34.342424,
                "latitude": 12.333456
            },
            "user_id": 1
        }
    }

    or

    {"user_data":
        {
            "user_id": 1
        }
    }

    or even

    {"time": 1232131231}

    so when we got one element inside our JSON request NetCatKS internally will looking
    for API's from a type IJSONResourceAPI and all of them have to implement process_factory
    method, it will be called as callback when we got a request.

    How the API will recognize which API to call?

    Here we talking for a API called root API, and NetCatKS will looking for API name that
    response on the our root element name or:

    @implementer(IJSONResourceAPI):
    class MyTestAPI(object):

        adapts(IJSONResource)

        def __init__(self, factory_json):
            self.factory = factory_json

        def process_factory(self):

            print self.factory.to_dict()
            # here we dealing with our request for the fist time

            # and we have to return IJSONResource implementation
            # we also can define additional DProtocol structures
            # that can be used here, for our response instead self.factory

            return self.factory


    will trigger on a request with structure like {"mytestapi": ""}
    and all the data from the request will be passed to our API constructor
    as first argument. Then  NetCatKS will call process_factory, the place when
    you have to deal with this data.

    @implementer(IJSONResourceAPI)
    class Convert(object):

        adapts(IJSONResource)

        def __init__(self, factory_json):
            self.factory = factory

        def process_factory(self):

            self.factory.convert.id = 4200
            return self.factory

    as above one but will trigger on {"convert": ""}

    If the service that require this API is a TCP or a WEB the result
    will be returned to the client immediately, but if the service is a WAMP
    the result will be redirected to our global subscriber from where you have
    possibility to publish this data to another subscribers.

    All API's which are registered under this interface have to be registered as
    subscriber adapters and will fire when protocol from DProtocol type or other
    IJSONResource comes as request.
    """

    def process_factory():
        """

        :return: IJSONResource
        """


class IJSONResourceAPI(Interface):

    """

    The implementer have to keep the schema like so:

    1. the request:

        {"command": "event", "id": 42, "clock": 1441461133.176596}

    2. Make API that have a mirror attributes for mapping
    so if the request has key command with value event,
    we can write the IJSONResourceAPI implementation like this:

        @implementer(IJSONResourceAPI)
        class Command(object):

            adapts(IJSONResource)

            def __init__(self, adapter):
                self.adapter = adapter

            def event(self):
                # works here with self.adapter
    """


class IXMLResourceAPI(Interface):
    """
    marker for API's which support IXMLResource
    """