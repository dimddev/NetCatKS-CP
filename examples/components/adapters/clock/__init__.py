from datetime import datetime

from NetCatKS.Logger import Logger
from NetCatKS.Components import BaseRootAPIWampMixin


class Clock(BaseRootAPIWampMixin):

    def __init__(self, factory=None):

        super(Clock, self).__init__(factory)

        self.logger = Logger()

    @staticmethod
    def print_result_callback(res, factory):

        factory.clock = res
        return factory

    @staticmethod
    def print_result_callback_error(err):
        print err
        return False

    def process_factory(self):

        self.logger.debug(self.factory.to_dict())

        # we trying to get a wamo session
        session = self.get_session()

        # if exist we will get the time from a rpc with a name 'get_time'
        # registered as wamp component inside components/wamp/rpc
        if session:

            result = session.call('get_time')

            result.addCallback(self.print_result_callback, self.factory)
            result.addErrback(self.print_result_callback_error)

            return result

        else:

            # if does not exist
            self.factory.clock = str(datetime.now())
            return self.factory