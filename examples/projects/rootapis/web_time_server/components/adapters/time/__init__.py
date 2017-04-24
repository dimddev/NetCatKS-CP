from datetime import datetime

from NetCatKS.Logger import Logger
from NetCatKS.Components import BaseRootAPI


class Time(BaseRootAPI):

    def __init__(self, factory):

        super(Time, self).__init__(factory)

        self.factory = factory
        self.logger = Logger()

    def process_factory(self):
        
        if self.factory.time == 'get':
            self.factory.time = str(datetime.now())

        else:
            self.factory.time = 'service unavailable'

        self.logger.debug('IN TIME API: {}'.format(self.factory.to_dict()))

        return self.factory

