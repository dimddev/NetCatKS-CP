from NetCatKS.Components import BaseWampComponent
from autobahn import wamp


class TestComponentWamp(BaseWampComponent):

    def __init__(self):
        super(TestComponentWamp, self).__init__()

    @wamp.register(u'hot_news_publisher')
    def pub_news(self):

        import time
        self.session.publish('hot_news', time.time())

    @wamp.register(u'hot_news_subscriber')
    def hot_news_subscriber(self):

        def subscribe_discpatcher(result):
            print(result)

        self.session.subscribe(subscribe_discpatcher, u'hot_news_sub')