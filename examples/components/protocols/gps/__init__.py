from zope.interface import Interface, Attribute, implementer

from NetCatKS.DProtocol import BaseProtocolActions, DynamicProtocol
from NetCatKS.Components import RequestSubscriber


class IGPSUser(Interface):

    username = Attribute("username of user")
    email = Attribute("email of user")


@implementer(IGPSUser)
class GPSUserProtocol(BaseProtocolActions):

    def __init__(self):

        self.__username = None
        self.__email = None

    @property
    def username(self):
        return self.__username

    @username.setter
    def username(self, user):
        self.__username = user

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, email):
        self.__email = email


class IGPSCoordinates(Interface):

    long = Attribute("longitude of user")
    lat = Attribute("latitude of user")


@implementer(IGPSCoordinates)
class GPSCoordinatesProtocol(BaseProtocolActions):

    def __init__(self):

        self.__long = None
        self.__lat = None

    @property
    def long(self):
        return self.__long

    @long.setter
    def long(self, long):
        self.__long = long

    @property
    def lat(self):
        return self.__lat

    @lat.setter
    def lat(self, lat):
        self.__lat = lat


class IGPSProtocol(Interface):

    profile = Attribute('object represent user profile')
    coordinates = Attribute('object represented coordiantes')


@implementer(IGPSProtocol)
class GPSProtocolImplementer(DynamicProtocol):

    def __init__(self, **kwargs):

        super(GPSProtocolImplementer, self).__init__(**kwargs)

        self.__profile = GPSUserProtocol()

        self.__coordinates = GPSCoordinatesProtocol()

    @property
    def profile(self):
        return self.__profile

    @profile.setter
    def profile(self, kwargs):
        self.check_for_dict(kwargs)
        self.__profile = self.public_setter(kwargs, self.__profile)

    @property
    def coordinates(self):
        return self.__coordinates

    @coordinates.setter
    def coordinates(self, kwargs):
        self.check_for_dict(kwargs)
        self.__coordinates = self.public_setter(kwargs, self.__coordinates)


class GPSProtocol(GPSProtocolImplementer, RequestSubscriber):

    def __init__(self, **kwargs):

        super(GPSProtocol, self).__init__(**kwargs)

__all__ = [
    'IGPSUser',
    'GPSUserProtocol',
    'IGPSProtocol',
    'GPSProtocol',
    'IGPSCoordinates',
    'GPSCoordinatesProtocol',
]