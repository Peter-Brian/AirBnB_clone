#!/usr/bin/python3
"""
Test User Class - Comproving expectect outputs and documentation
"""

from datetime import datetime
import models
import pep8
import inspect
import unittest
from unittest import mock
import time


User = models.user.User
mod_doc = models.user.__doc__


class TestDocs(unittest.TestCase):
    """Test documentation and style"""
    @classmethod
    def setUpClass(self):
        """Setup for dosctring"""
        user_i = inspect.getmembers(User, inspect.isfunction)

    def test_pep8_conformance_user(self):
        """testing pep8 in user.py"""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/user.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_module_docstring(self):
        """Test for the existence of module docstring"""
        self.assertIsNot(mod_doc, None,
                         "base_model.py needs a docstring")
        self.assertTrue(len(mod_doc) > 1,
                        "base_model.py needs a docstring")

    def test_dosctring(self):
        """Testing documentation"""
        self.assertIsNot(mod_doc, None,
                         "base_model.py needs a doctring")
        self.assertTrue(len(mod_doc) > 1,
                        "base_model.py needs a docstring")


class TestBaseModel(unittest.TestCase):
    """testing BaseModel Class"""
    @mock.patch('models.user')
    def test_instances(self, mock_storage):
        """Testing that object is correctly created"""
        instance = User()
        self.assertIs(type(instance), User)
        instance.name = "Holberton"
        instance.number = 89
        instance.email = "Holberton@holbertonshool.com"
        instance.password = "tubbcito-plumplum"
        instance.first_name = "joshua"
        instance.last_name = "joshua2"

        expectec_attrs_types = {
            "id": str,
            "created_at": datetime,
            "updated_at": datetime,
            "name": str,
            "number": int,
            "email": str,
            "password": str,
            "first_name": str,
            "last_name": str
        }
        # testing types and attr names
        for attr, types in expectec_attrs_types.items():
            with self.subTest(attr=attr, typ=types):
                self.assertIn(attr, instance.__dict__)
                self.assertIs(type(instance.__dict__[attr]), types)
        self.assertEqual(instance.name, "Holberton")
        self.assertEqual(instance.number, 89)
        self.assertEqual(instance.email, "Holberton@holbertonshool.com")
        self.assertEqual(instance.first_name, "joshua")
        self.assertEqual(instance.last_name, "joshua2")

    def test_datetime(self):
        """testing correct datetime assignation
        correct assignation of created_at and updated_at"""
        created_at = datetime.now()
        instance1 = User()
        updated_at = datetime.now()
        self.assertEqual(created_at <= instance1.created_at
                         <= updated_at, True)
        time.sleep(1)
        created_at = datetime.now()
        instance2 = User()
        updated_at = datetime.now()
        self.assertTrue(created_at <= instance2.created_at <= updated_at, True)
        self.assertEqual(instance1.created_at, instance1.created_at)
        self.assertEqual(instance2.updated_at, instance2.updated_at)
        self.assertNotEqual(instance1.created_at, instance2.created_at)
        self.assertNotEqual(instance1.updated_at, instance2.updated_at)

    def test_uuid(self):
        """testing uuid"""
        instance1 = User()
        instance2 = User()
        for instance in [instance1, instance2]:
            tuuid = instance.id
            with self.subTest(uuid=tuuid):
                self.assertIs(type(tuuid), str)

        self.assertNotEqual(instance1.id, instance2.id)

    def test_dictionary(self):
        """testing to_dict correct funtionality"""
        """Testing that object is correctly created"""
        instance3 = User()
        self.assertIs(type(instance3), User)
        instance3.name = "Holbies"
        instance3.number = 89
        instance3.email = "Holberton@holbertonshool.com"
        instance3.password = "tubbcito-plumplum"
        instance3.first_name = "joshua"
        instance3.last_name = "joshua2"
        new_inst = instance3.to_dict()
        expectec_attrs = ["id",
                          "created_at",
                          "updated_at",
                          "name",
                          "number",
                          "email",
                          "password",
                          "first_name",
                          "last_name",
                          "__class__"]
        self.assertCountEqual(new_inst.keys(), expectec_attrs)
        self.assertEqual(new_inst['__class__'], 'User')
        self.assertEqual(new_inst['last_name'], 'joshua2')
        self.assertEqual(new_inst['first_name'], 'joshua')
        self.assertEqual(new_inst['name'], 'Holbies')
        self.assertEqual(new_inst['number'], 89)
        self.assertEqual(new_inst['email'], 'Holberton@holbertonshool.com')
        self.assertEqual(new_inst['password'], 'tubbcito-plumplum')

    def test_str_method(self):
        """testing str method, checking output"""
        instance4 = User()
        strr = "[User] ({}) {}".format(instance4.id, instance4.__dict__)
        self.assertEqual(strr, str(instance4))

    @mock.patch('models.storage')
    def test_save_method(self, mock_storage):
        """test save method and if it updates
        "updated_at" calling storage.save"""
        instance4 = User()
        created_at = instance4.created_at
        updated_at = instance4.updated_at
        instance4.save()
        new_created_at = instance4.created_at
        new_updated_at = instance4.updated_at
        self.assertNotEqual(updated_at, new_updated_at)
        self.assertEqual(created_at, new_created_at)
        self.assertTrue(mock_storage.save.called)


if __name__ == "__main__":
    unittest.main()
