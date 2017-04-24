from __future__ import absolute_import

__author__ = 'dimd'

import unittest

from zope.interface.verify import verifyObject
from zope.interface.exceptions import DoesNotImplement

from NetCatKS.DProtocol import BaseProtocolActions, DynamicProtocol
from NetCatKS.DProtocol.api.public.storage import ProtocolStorage
from NetCatKS.DProtocol.api.interfaces.storage import IProtocolStogareInterface


class TestProtoclDetails(BaseProtocolActions):

    def __init__(self):

        self.__age = None
        self.__city = None
        self.__jobs = []

    @property
    def age(self):
        return self.__age

    @age.setter
    def age(self, age):
        self.__age = age

    @property
    def city(self):
        return self.__city

    @city.setter
    def city(self, city):
        self.__city = city

    @property
    def jobs(self):
        return self.__jobs

    @jobs.setter
    def jobs(self, jobs):
        self.__jobs = self.if_list_auto_append(jobs, self.__jobs, 4)


class TestProtocolProfile(BaseProtocolActions):

    def __init__(self):

        self.__name = None
        self.__email = None
        self.__details = TestProtoclDetails()

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, e):
        self.__email = e

    @property
    def details(self):
        return self.__details

    @details.setter
    def details(self, details):
        self.__details = self.public_setter(details, self.__details)


class TestProtoclUser(DynamicProtocol):

    def __init__(self, **kwargs):

        super(TestProtoclUser, self).__init__(**kwargs)

        self.__profile = TestProtocolProfile()
        self.__location = []
        self.__max_length = []

    @property
    def profile(self):
        return self.__profile

    @profile.setter
    def profile(self, profile):
        self.__profile = self.public_setter(profile, self.__profile)

    @property
    def location(self):
        return self.__location

    @location.setter
    def location(self, location):
        self.__location = self.if_list_auto_append(location, self.__location)

    @property
    def max_length(self):
        return self.__max_length

    @max_length.setter
    def max_length(self, add_len):
        self.__max_length = self.if_list_auto_append(add_len, self.__max_length, 144)


class TestDprotocol(unittest.TestCase):

    def setUp(self):

        self.init_profile()
        self.init_user()

    def init_profile(self):

        self.profile = TestProtocolProfile()
        self.profile.name = 'name1'
        self.profile.email = 'email1@email.com'

    def test_to_dict_profile(self):

        self.assertDictEqual(
            self.profile.to_dict(),
            {'details': {'city': None, 'age': None, 'jobs': []}, 'name': 'name1', 'email': 'email1@email.com'}
        )

    def init_user(self):

        self.user = TestProtoclUser()
        self.user.id = 1234567
        self.user.location = 'here'
        self.user.location = 'there'
        self.user.location = 'there, here'
        self.user.profile.name = 'name2'
        self.user.profile.email = 'email2@email.com'
        self.user.profile.details.age = 34
        self.user.profile.details.jobs = 'Developer'
        self.user.profile.details.jobs = 'Art'
        self.user.profile.details.city = 'Frankfurt'

    def test_constructor(self):

        with self.assertRaises(DoesNotImplement):
            TestProtoclUser(storage=object)

    def test_public_setter(self, num=None):

        if num is None:

            self.user.profile = {
                'name': 'public_name',
                'email': 'public@email.com'
            }

            self.assertEquals(self.user.profile.name, 'public_name')
            self.assertEquals(self.user.profile.email, 'public@email.com')

            with self.assertRaises(AttributeError):

                self.user.profile = {
                    'name': 'public_name',
                    'title': 'tittle'
                }

    def test_public_setter_many(self, num=None):

        for x in range(1, 9421):

            self.user.profile = {
                'name': 'public_name_{}'.format(x),
                'email': 'public_{}@email.com'.format(x)
            }

            self.assertEquals(self.user.profile.name, 'public_name_{}'.format(x))
            self.assertEquals(self.user.profile.email, 'public_{}@email.com'.format(x))

    def test_get_storage(self):

        st = self.user.get_storage()

        self.assertDictEqual({}, st)

    def test_save(self):

        self.user.save()

        user = self.user.get_session(id=1234567)
        self.assertEqual(self.user.id, user.id)

        self.user.id = None

        with self.assertRaises(ValueError):
            self.user.save()

        with self.assertRaises(NotImplementedError):
            self.profile.save()

        self.test_to_object(user)

    def test_finish(self):

        self.user.save()
        self.assertEquals(self.user.id, self.user.get_session(id=1234567).id)

        self.user.finish()
        self.assertFalse(self.user.get_session(id=1234567))

    def test_flush_storage(self):

        self.user.save()

        self.assertEquals(self.user.id, self.user.get_session(id=1234567).id)

        self.user.flush_storage()
        
        self.assertDictEqual({}, self.user.get_storage())

    def test_add_session_get_session(self):

        self.user.id = 42

        self.user.add_session(id=self.user.id, session=self.user)

        with self.assertRaises(AttributeError):
            self.user.add_session(id=self.user.id)

        with self.assertRaises(AttributeError):
            self.user.add_session(session='')

        self.assertFalse(self.user.add_session(id=self.user.id, session=self.user))

        with self.assertRaises(AttributeError):
            self.user.get_session()

        user = self.user.get_session(id=4242)

        self.assertFalse(user)

        user = self.user.get_session(id=42)

        self.assertEquals(user.id, self.user.id)

        with self.assertRaises(AttributeError):
            self.user.add_session(id=self.user.id, session=object)

        self.test_to_object(user)

    def test_add_session_get_session_many_to_object(self):

        for x in range(1, 9421):

            self.init_user()

            self.user.profile.name = 'user_{}'.format(x)
            self.user.profile.email = 'email_{}@email.com'.format(x)

            self.user.id = x
            self.user.add_session(id=x, session=self.user)

            user = self.user.get_session(id=x)
            # print user
            self.assertEquals('user_{}'.format(x), user.profile.name)
            self.assertEquals('email_{}@email.com'.format(x), user.profile.email)
            self.test_to_object(user)

    def test_get_all_keys(self):

        all_keys = self.user.get_all_keys()
        all_keys.sort()

        self.user_temp = TestProtoclUser()

        all_keys2 = self.user_temp.get_all_keys()
        all_keys2.sort()

        self.assertListEqual(all_keys, all_keys2)

    def test_to_tdo(self):

        req = {'age': None, 'city': None, 'location': []}
        req1 = {'id': None, 'user': None, 'email': None, 'age': None}

        self.user.location = 'one'
        self.user.location = 'two'
        self.user.location = 'three'

        self.assertDictEqual(req, self.user.to_tdo(req))
        self.assertDictEqual(req1, self.user.to_tdo(req1))

        self.assertListEqual(req.get('location'), self.user.location)
        self.assertEqual(len(req.get('location')), len(self.user.location))

    def test_to_json(self):

        origin = '{"profile": {"details": {"city": "Frankfurt", "age": 34, "jobs": ["Developer", "Art"]}, "name": "name2", "email": "email2@email.com"}, "max_length": [], "location": ["here", "there", "there, here"], "id": 1234567}'
        self.assertEquals(origin, self.user.to_json())

        json_indent = self.user.to_json(indent=4)
        json_indent = json_indent.replace('\n', '')
        json_indent = json_indent.replace(' ', '')
        self.assertEquals(json_indent, origin.replace(' ', ''))

    def test_to_object(self, out_object=None):

        if out_object:
            out_object = out_object.to_dict()

        d = out_object or self.user.to_dict()

        o = self.user_temp = TestProtoclUser()

        d1 = o.to_object(d)

        self.assertFalse(o.to_object())

        self.assertEqual(self.user.profile.name, d1.profile.name)
        self.assertEqual(self.user.profile.email, d1.profile.email)
        self.assertEqual(self.user.id, d1.id)

        self.assertListEqual(self.user.profile.details.jobs, d1.profile.details.jobs)
        self.assertEquals(len(self.user.profile.details.jobs), 2)
        self.assertEquals(len(d1.profile.details.jobs), 2)

        self.assertListEqual(['here', 'there', 'there, here'], d1.location)
        self.assertListEqual(['here', 'there', 'there, here'], self.user.location)

        self.assertDictEqual(d, d1.to_dict())

    def test_to_xml(self):

        with self.assertRaises(ValueError):
            self.user.to_xml()

        with self.assertRaises(ValueError):
            self.user.to_xml([])

        root = {'root': {'id': 4, 'username': 'user'}}

        xml_output = '<?xml version="1.0" encoding="utf-8"?><root><username>user</username><id>4</id></root>'

        xml = self.user.to_xml(root).replace('\n', '')
        self.assertEquals(xml, xml_output)

    def test_if_list_auto_append(self):

        over = range(0, 3500)

        with self.assertRaises(OverflowError):
            self.user.max_length = over

        self.user.max_length = {}

        self.assertEqual(list, type(self.user.max_length))

        for x in over * 2:
            self.user.max_length = x

        self.assertEqual(144, len(self.user.max_length))

        self.assertEqual(3499, self.user.max_length[-1])

        with self.assertRaises(TypeError):

            self.user.if_list_auto_append(1, {}, 144)

        with self.assertRaises(TypeError):
            self.user.if_list_auto_append(1, None, 144)

        self.user.max_length = range(1, 100)
        self.assertListEqual(self.user.max_length, range(1, 100))

    def test_check_for_float_and_int(self):

        self.assertTrue(self.user.check_for_float_and_int(1))
        self.assertTrue(self.user.check_for_float_and_int(1.1))

        with self.assertRaises(TypeError):
            self.user.check_for_float_and_int('87654')

        with self.assertRaises(TypeError):
            self.user.check_for_float_and_int([])

    def test_check_for_float(self):

        with self.assertRaises(TypeError):
            self.user.check_for_float(1)

        self.assertTrue(self.user.check_for_float(1.134))
        self.assertTrue(self.user.check_for_float(178.134))

    def test_check_for_int(self):

        with self.assertRaises(TypeError):
            self.user.check_for_int(1.1)

        self.assertTrue(self.user.check_for_int(1))

    def test_check_for_list(self):

        with self.assertRaises(TypeError):
            self.user.check_for_int(())

        with self.assertRaises(TypeError):
            self.user.check_for_int({})

        self.assertTrue(self.user.check_for_list([]))

    def test_check_for_dict(self):

        with self.assertRaises(TypeError):
            self.user.check_for_dict([])

        with self.assertRaises(TypeError):
            self.user.check_for_dict(())

        self.assertTrue(self.user.check_for_dict({}))

    def test_check_for_bool(self):

        with self.assertRaises(TypeError):
            self.user.check_for_bool(1)

        with self.assertRaises(TypeError):
            self.user.check_for_bool(0)

        self.assertTrue(self.user.check_for_bool(True))
        self.assertTrue(self.user.check_for_bool(False))

    def test_verify_storage(self):

        ps = ProtocolStorage()

        class FakeStorage(object):
            pass

        self.assertTrue(IProtocolStogareInterface.providedBy(ps))
        self.assertTrue(verifyObject(IProtocolStogareInterface, ps))

        with self.assertRaises(DoesNotImplement):

            verifyObject(IProtocolStogareInterface, {})

        with self.assertRaises(DoesNotImplement):

            verifyObject(IProtocolStogareInterface, object)

        with self.assertRaises(DoesNotImplement):
            verifyObject(IProtocolStogareInterface, FakeStorage())

#dprotocol_suite = unittest.TestLoader().loadTestsFromTestCase(TestDprotocol)
#unittest.TextTestRunner(verbosity=2).run(dprotocol_suite)
