from NetCatKS.Components import BaseAPI, BaseRootAPI
from NetCatKS.Logger import Logger


log = Logger()


class Command(BaseAPI):

    def __init__(self, factory):
        super(Command, self).__init__(factory)

    def event(self):

        log.info('TIME API ADAPTER: {}'.format(self.factory.id))
        self.factory.id = 10
        return self.factory


class Convert(BaseRootAPI):

    def __init__(self, factory):
        super(Convert, self).__init__(factory)

    def process_factory(self):

        self.factory.convert.id = 4200
        return self.factory