#!/usr/bin/python3
"""Test Storage- Comproving expectect outputs and documentation"""

import models
import inspect
import json
import os
import unittest
from datetime import datetime
from models.engine import file_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.state import State
# import pep8
from models.user import User
from models.review import Review

FileStorage = file_storage.FileStorage
classes = {"BaseModel": BaseModel, "User": User, "State": State,
           "Place": Place, "City": City, "Amenity": Amenity, "Review": Review}


class TestFileStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of FileStorage class"""
    @classmethod
    def setUpClass(cls):
        """setting up doc tests"""
        cls.fs_f = inspect.getmembers(FileStorage, inspect.isfunction)

    # def test_pep8_file_storage(self):
    # """testing that file_storage passes pep8"""
    # pep81 = pep8.StyleGuide(quiet=True)
    # result = pep81.check_files(['models/engine/file_storage.py'])
    # self.assertEqual(result.total_errors, 0,
    # "Found code style errors (and warnings).")

    # def test_pep8_test_engine(self):
    # """testing that test_engine passes pep8"""
    # pep8s = pep8.StyleGuide(quiet=True)
    # result = pep8s.check_files(['tests/test_models/test_engine/\
    # test_file_storage.py'])
    # self.assertEqual(result.total_errors, 0,
    # "Found code style errors (and warnings).")

    def test_docstring_file_storage(self):
        """testing doscrting for file_storage"""
        self.assertIsNot(file_storage.__doc__, None,
                         "file_storage.py needs a docstring")
        self.assertTrue(len(file_storage.__doc__) >= 1,
                        "file_storage.py needs a docstring")


class TestFileStorage(unittest.TestCase):
    """Testin filestorage class"""
    def test_all_returns_dict(self):
        """testing types and objesta equality"""
        storage = FileStorage()
        new_dict = storage.all()
        self.assertEqual(type(new_dict), dict)
        self.assertIs(new_dict, storage._FileStorage__objects)

    def test_new_method(self):
        """testing that  new method saves on __objects attr"""
        storage = FileStorage()
        save = FileStorage._FileStorage__objects
        FileStorage._FileStorage__objects = {}
        test_dict = {}
        for key, value in classes.items():
            with self.subTest(key=key, value=value):
                instance = value()
                instance_key = instance.__class__.__name__ + "." + instance.id
                storage.new(instance)
                test_dict[instance_key] = instance
                self.assertEqual(test_dict, storage._FileStorage__objects)
        FileStorage._FileStorage__objects = save

    def test_save(self):
        """Testing proper behaviour saving in file.json"""
        os.remove("file.json")
        storage = FileStorage()
        new_dict = {}
        for key, value in classes.items():
            instance = value()
            instance_key = instance.__class__.__name__ + "." + instance.id
            new_dict[instance_key] = instance
        save = FileStorage._FileStorage__objects
        FileStorage._FileStorage__objects = new_dict
        storage.save()
        FileStorage._FileStorage__objects = save
        for key, value in new_dict.items():
            new_dict[key] = value.to_dict()
        string = json.dumps(new_dict)
        with open("file.json", "r") as f:
            js = f.read()
        self.assertEqual(json.loads(string), json.loads(js))
