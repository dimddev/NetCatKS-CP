__author__ = 'dimd'

from twisted.web.resource import Resource

from NetCatKS.NetCAT.api.interfaces.twisted.recources import IDefaultWebResource
from NetCatKS.NetCAT.api.interfaces.twisted.factories import IDefaultWebFactory
from NetCatKS.Logger import Logger

from zope.interface import classImplementsOnly
from zope.component import adapts, getGlobalSiteManager

from NetCatKS.Dispatcher import IDispatcher, DispathcherResultHelper
from NetCatKS.Validators import Validator


class BaseWebMethods(object):

    def __init__(self):

        self.__logger = Logger()

    def render_PUT(self, request):

        return 'ok'

    def render_GET(self, request):
        """

        :param request:
        :return:
        """

        print request
        return """
<!DOCTYPE html>
<head>
    <title>IplayNinja</title>
    <link rel="stylesheet" type="text/css" href="ninja.css">
</head>
<body>
    <h1>Hello from NetCatKS Web</h1>
</body>
</html>
"""

    def render_POST(self, request):

        """

        :param request:
        :return:
        """

        result = IDispatcher(Validator(request.content.read())).dispatch()
        result_response = DispathcherResultHelper(result)
        return result_response.result_validation(None, None, 'WEB')


class DefaultWebResource(Resource):

    adapts(IDefaultWebFactory)

    isLeaf = True

    def __init__(self, factory, **kwargs):
        """

        :param factory:
        :param kwargs:
        :return:
        """

        base = BaseWebMethods()
        self.__logger = Logger()

        for meth in factory.config.http_methods:

            try:

                name = 'render_{}'.format(meth)
                web_resource = getattr(base, name)

            except AttributeError as e:

                allow_methods = [
                    render.replace('render_', '') for render in base.__class__.__dict__ if render.startswith('render')
                ]

                print('[ !!!!! Warning: ] Ivalid web methods was provided, available are: {}, error: {}'.format(
                    ', '.join(allow_methods), e
                ))

            else:
                setattr(DefaultWebResource, name, web_resource)

        Resource.__init__(self)


classImplementsOnly(DefaultWebResource, IDefaultWebResource)

gsm = getGlobalSiteManager()
gsm.registerAdapter(DefaultWebResource)
