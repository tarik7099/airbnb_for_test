#!/usr/bin/python3
"""The Unittest module for BaseModel Class."""

from models import storage
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from datetime import datetime
import json
import os
import re
import time
import unittest
import uuid


class TestBaseModel(unittest.TestCase):

    """Test  Cases for BaseModel class."""

    def setUp(self):
        """Sets up the test methods"""
        pass

    def tearDown(self):
        """Tears down the test methods"""
        self.resetStorage()
        pass

    def resetStorage(self):
        """Resets the FileStorage data."""
        FileStorage._FileStorage__objects = {}
        if os.path.isfile(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)

    def test3_instantiation(self):
        """Tests instantiation of the BaseModel class"""

        bs = BaseModel()
        self.assertEqual(str(type(bs)), "<class 'models.base_model.BaseModel'>")
        self.assertIsInstance(bs, BaseModel)
        self.assertTrue(issubclass(type(bs), BaseModel))

    def test3_init_no_args(self):
        """Tests thz  __init__ with no args"""
        self.resetStorage()
        with self.assertRaises(TypeError) as ee:
            BaseModel.__init__()
        mesg = "__init__() missing 1 required positional argument: 'self'"
        self.assertEqual(str(ee.exception), mesg)

    def test3_init_many_args(self):
        """Tests __init__ with many args"""
        self.resetStorage()
        args = [i for i in range(1000)]
        bs = BaseModel(0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
        bs = BaseModel(*args)

    def test3_attributes(self):
        """Tests attributes value for the instance of BaseModel class"""

        attributes = storage.attributes()["BaseModel"]
        bs = BaseModel()
        for k, v in attributes.items():
            self.assertTrue(hasattr(bs, k))
            self.assertEqual(type(getattr(bs, k, None)), v)

    def test3_datetime_created(self):
        """Test if updated_at and created_at are current at the creation"""
        dt_now = datetime.now()
        bs = BaseModel()
        df = bs.updated_at - bs.created_at
        self.assertTrue(abs(df.total_seconds()) < 0.01)
        df = bs.created_at - dt_now
        self.assertTrue(abs(df.total_seconds()) < 0.1)

    def test3_id(self):
        """Tests for the unique user ids"""

        ld = [BaseModel().id for i in range(1000)]
        self.assertEqual(len(set(ld)), len(ld))

    def test3_save(self):
        """Tests public instance method save()."""

        bs = BaseModel()
        time.sleep(0.5)
        dt_now = datetime.now()
        bs.save()
        df = bs.updated_at - dt_now
        self.assertTrue(abs(df.total_seconds()) < 0.01)

    def test3_str(self):
        """Test for the __str__ method."""
        bs = BaseModel()
        rex = re.compile(r"^\[(.*)\] \((.*)\) (.*)$")
        rs = rex.match(str(bs))
        self.assertIsNotNone(rs)
        self.assertEqual(rs.group(1), "BaseModel")
        self.assertEqual(rs.group(2), bs.id)
        s = rs.group(3)
        s = re.sub(r"(datetime\.datetime\([^)]*\))", "'\\1'", s)
        d = json.loads(s.replace("'", '"'))
        d2 = bs.__dict__.copy()
        d2["created_at"] = repr(d2["created_at"])
        d2["updated_at"] = repr(d2["updated_at"])
        self.assertEqual(d, d2)

    def test3_to_dict(self):
        """Test public instance method to_dict()"""

        bs = BaseModel()
        bs.name = "Laura"
        bs.age = 23
        d = bs.to_dict()
        self.assertEqual(d["id"], bs.id)
        self.assertEqual(d["__class__"], type(bs).__name__)
        self.assertEqual(d["created_at"], bs.created_at.isoformat())
        self.assertEqual(d["updated_at"], bs.updated_at.isoformat())
        self.assertEqual(d["name"], bs.name)
        self.assertEqual(d["age"], bs.age)

    def test3_to_dict_no_args(self):
        """Test to_dict() with no args."""
        self.resetStorage()
        with self.assertRaises(TypeError) as ee:
            BaseModel.to_dict()
        mesg = "to_dict() missing 1 required positional argument: 'self'"
        self.assertEqual(str(ee.exception), mesg)

    def test3_to_dict_excess_args(self):
        """Test to_dict() with too many args"""
        self.resetStorage()
        with self.assertRaises(TypeError) as ee:
            BaseModel.to_dict(self, 98)
        mesg = "to_dict() takes 1 positional argument but 2 were given"
        self.assertEqual(str(ee.exception), mesg)

    def test4_instantiation(self):
        """Test instantiation with **kwargs"""

        my_model = BaseModel()
        my_model.name = "Holberton"
        my_model.my_number = 89
        my_model_json = my_model.to_dict()
        new_model = BaseModel(**my_model_json)
        self.assertEqual(new_model.to_dict(), my_model.to_dict())

    def test4_instantiation_dict(self):
        """Test instantiation with **kwargs frm custom dict."""
        dt = {"__class__": "BaseModel",
             "updated_at":
             datetime(2050, 12, 30, 23, 59, 59, 123456).isoformat(),
             "created_at": datetime.now().isoformat(),
             "id": uuid.uuid4(),
             "var": "foobar",
             "int": 108,
             "float": 3.14}
        bs = BaseModel(**dt)
        self.assertEqual(bs.to_dict(), dt)

    def test5_save(self):
        """Test storage.save() is called from save()."""
        self.resetStorage()
        bs = BaseModel()
        bs.save()
        key = "{}.{}".format(type(bs).__name__, bs.id)
        dt = {key: bs.to_dict()}
        self.assertTrue(os.path.isfile(FileStorage._FileStorage__file_path))
        with open(FileStorage._FileStorage__file_path,
                  "r", encoding="utf-8") as fl:
            self.assertEqual(len(fl.read()), len(json.dumps(dt)))
            fl.seek(0)
            self.assertEqual(json.load(fl), dt)

    def test5_save_no_args(self):
        """Test save() with no args."""
        self.resetStorage()
        with self.assertRaises(TypeError) as ee:
            BaseModel.save()
        mesg = "save() missing 1 required positional argument: 'self'"
        self.assertEqual(str(ee.exception), mesg)

    def test5_save_excess_args(self):
        """Tests save() with too many args."""
        self.resetStorage()
        with self.assertRaises(TypeError) as ee:
            BaseModel.save(self, 98)
        mesg = "save() takes 1 positional argument but 2 were given"
        self.assertEqual(str(ee.exception), mesg)


if __name__ == '__main__':
    unittest.main()
