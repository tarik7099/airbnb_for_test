#!/bin/usr/python3
from base_model import BaseModel
from user import User

user1 = User()
print(str(user1))
dict_rep = user1.to_dict()
print(dict_rep)
str_rep = user1.__str__()
print(str_rep)