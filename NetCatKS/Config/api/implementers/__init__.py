__author__ = 'dimd'

import json

from NetCatKS.Config.api.interfaces import IConfig
from NetCatKS.Config.api.implementers.configuration import *

from zope.interface import implementer
from zope.component import createObject


@implementer(IConfig)
class Config(object):

    """
    Trying to load config/config.json file and then load as JSON
    """

    __instance = None
    __config = None

    def __new__(cls):

        if Config.__instance is None:

            Config.__instance = object.__new__(cls)

            try:

                with open('config/config.json', 'r') as config:
                    Config.__config = json.loads(config.read(), encoding='utf-8')

            except Exception as e:
                raise Exception('Config not found: {}'.format(e.message))

            else:

                config.close()

        return Config.__instance

    def __init__(self):
        pass

    def get(self, section):
        return self.__class__.__config.get(section, None)

    @classmethod
    def __get_section(cls, section):

        proto = createObject(section)

        if section.upper() in cls.__config:
            return proto.to_object(cls.__config.get(section.upper()))

    @classmethod
    def get_tcp(cls):
        return cls.__get_section('tcp')

    @classmethod
    def get_web(cls):
        return cls.__get_section('web')

    @classmethod
    def get_wamp(cls):
        return cls.__get_section('wamp')


    @classmethod
    def get_ws(cls):
        return cls.__get_section('ws')


__all__ = [
    'Config',
    'TCP',
    'WS',
    'WAMP',
    'WEB'
]
