__author__ = 'dimd'

from autobahn.wamp.types import ComponentConfig
from autobahn.websocket.protocol import parseWsUrl
from autobahn.twisted.websocket import WampWebSocketClientFactory

from twisted.internet import reactor
from twisted.internet.endpoints import clientFromString
from twisted.application import service

from NetCatKS.Logger import Logger
from NetCatKS.NetCAT.api.public import IDefaultAutobahnFactory
from NetCatKS.NetCAT.api.implementers.autobahn.factories.ws import DefaultWSFactory
from NetCatKS.Config.api.implementers.configuration.wamp import WAMP

from zope.interface import implementer


class Reconnect(object):

    def __init__(self, **kwargs):

        if 'session' not in kwargs or 'runner' not in kwargs:
            raise Exception('session is not provided')

        self.__session = kwargs['session']
        self.__runner = kwargs['runner']

        self.logger = Logger()
        self.config = kwargs.get('config')

    def start(self):

        try:

            self.logger.info(
                'TRYING TO CONNECT TO {}'.format(
                self.config
            ))

            run = self.__runner(config=self.config)
            run.run(self.__session)

        except Exception as e:
            self.logger.error('RECONNECTING ERROR: {}'.format(e.message))


@implementer(IDefaultAutobahnFactory)
class AutobahnDefaultFactory(service.Service):
    """
    This class is a convenience tool mainly for development and quick hosting
    of WAMP application components.

    It can host a WAMP application component in a WAMP-over-WebSocket client
    connecting to a WAMP router.
    """

    def __init__(self, **kwargs):
        """

        :param url: The WebSocket URL of the WAMP router to connect to (e.g. `ws://somehost.com:8090/somepath`)
        :type url: unicode
        :param realm: The WAMP realm to join the application session to.
        :type realm: unicode
        :param extra: Optional extra configuration to forward to the application component.
        :type extra: dict
        :param debug: Turn on low-level debugging.
        :type debug: bool
        :param debug_wamp: Turn on WAMP-level debugging.
        :type debug_wamp: bool
        :param debug_app: Turn on app-level debugging.
        :type debug_app: bool

        """

        self.logger = Logger()

        self.config = kwargs.get('config', None)

        if self.config is None:

            self.config = {}
            wamp = WAMP()

            self.logger.warning('Config is not provided failback to defaults')

            self.config.update({
                'protocol': 'wss',
                'hostname': 'localhost',
                'port': 8080, # integer
                'realm': 'realm1',
                'path': 'ws',
                'retry_interval': 2,  # in seconds
                'url': u'ws://localhost:8080/ws',
                'service_name': 'A Default WAMP Service name"'
            })

            self.config = wamp.to_object(self.config)

        self.url = kwargs.get('url', self.config.url)

        self.realm = u'{}'.format(kwargs.get('realm', self.config.realm))

        self.extra = kwargs.get('extra', dict())

        self.debug = kwargs.get('debug', False)

        self.debug_wamp = kwargs.get('debug_wamp', False)

        self.debug_app = kwargs.get('debug_app', False)

        self.belong_to = kwargs.get('belong_to', False)

        self.make = None

        self.protocol = kwargs.get('protocol', self.config.protocol)

        self.name = kwargs.get('name', self.config.service_name)

        self.port = kwargs.get('port', self.config.port)

        self.host = kwargs.get('host', self.config.hostname)

        self.path = kwargs.get('path', self.config.path)

    def run(self, make):
        """
        Run the application component.

        :param make: A factory that produces instances of :class:`autobahn.asyncio.wamp.ApplicationSession`
           when called with an instance of :class:`autobahn.wamp.types.ComponentConfig`.
        :type make: callable
        """

        isSecure, host, port, resource, path, params = parseWsUrl(self.url)

        ## start logging to console
        if self.debug or self.debug_wamp or self.debug_app:
            pass
            # log.startLogging(sys.stdout)

        ## factory for use ApplicationSession
        def create():

            cfg = ComponentConfig(self.realm, self.extra)

            try:
                session = make(config=cfg)

            except Exception as e:

                ## the app component could not be created .. fatal
                self.logger.critical('CREATE RUNNER EXCEPTION {}'.format(e.message))

            else:

                session.debug_app = self.debug_app
                return session

        ## create a WAMP-over-WebSocket transport client factory
        transport_factory = WampWebSocketClientFactory(
            create,
            url=self.url,
            debug=self.debug,
            debug_wamp=self.debug_wamp
        )

        if isSecure:
            endpoint_descriptor = "ssl:{0}:{1}".format(host, port)

        else:
            endpoint_descriptor = "tcp:{0}:{1}".format(host, port)

        try:
            self.logger.info('Trying to connect to: {}'.format(endpoint_descriptor))
            self.connect(endpoint_descriptor, transport_factory, make)

            return self

        except Exception as e:
            self.logger.error('CLIENT CONNECT ERROR: {}'.format(e.message))

    def connect(self, endpoint, transport, session):

        try:
            ## start the client from a Twisted endpoint

            client = clientFromString(reactor, endpoint)

            res = client.connect(transport)

            def connect_result(result):
                return result

            def connect_error(result):

                self.logger.error('CONNECTION ERROR: {}'.format(result.getErrorMessage()))

                try:

                    reconnect = Reconnect(
                        session=session,
                        runner=AutobahnDefaultFactory,
                        config=self.config
                    )

                    reactor.callLater(
                        self.config.retry_interval,
                        reconnect.start,
                    )

                except Exception as e:
                    self.logger.error('RECONNECTING ERROR: {}'.format(e.message))

            res.addCallback(connect_result)
            res.addErrback(connect_error)

            return res

        except Exception as e:
            self.logger.error('CONNECTION GLOBAL ERRORS: {}'.format(e.message))

    def startService(self):
        service.Service.startService(self)

    def stopService(self):
        service.Service.stopService(self)


__all__ = [
    'AutobahnDefaultFactory',
    'Reconnect',
    'DefaultWSFactory'
]
