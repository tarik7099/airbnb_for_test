#!/usr/bin/python3
"""A module contains the Base class for 
the AirBnB clone console.
"""

import uuid
from datetime import datetime
from models import storage


class BaseModel:

    """A Class for base model of object hierarchy"""

    def __init__(self, *args, **kwargs):
        """Initialization of Base instance

        Args:
            - *args: A list of args
            - **kwargs: A dict of key-values args
        """

        if kwargs is not None and kwargs != {}:
            for key in kwargs:
                if key == "created_at":
                    self.__dict__["created_at"] = datetime.strptime(
                        kwargs["created_at"], "%Y-%m-%dT%H:%M:%S.%f")
                elif key == "updated_at":
                    self.__dict__["updated_at"] = datetime.strptime(
                        kwargs["updated_at"], "%Y-%m-%dT%H:%M:%S.%f")
                else:
                    self.__dict__[key] = kwargs[key]
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            storage.new(self)

    def __str__(self):
        """Returns -> human-readable string representation
        of an instance."""

        return "[{}] ({}) {}".\
            format(type(self).__name__, self.id, self.__dict__)

    def save(self):
        """Updates updated_at attribute
        with the current datetime."""

        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """Returns -> dictionary representation of an instance."""

        my_dct = self.__dict__.copy()
        my_dct["__class__"] = type(self).__name__
        my_dct["created_at"] = my_dct["created_at"].isoformat()
        my_dct["updated_at"] = my_dct["updated_at"].isoformat()
        return my_dct
