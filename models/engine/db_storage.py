#!/usr/bin/python3
"""Defines the engine for MySQL database"""
from models.base_model import BaseModel, Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import os


user = os.getenv('HBNB_MYSQL_USER')
pwd = os.getenv('HBNB_MYSQL_PWD')
host = os.getenv('HBNB_MYSQL_HOST')
db = os.getenv('HBNB_MYSQL_DB')
env = os.getenv('HBNB_ENV')

class DBStorage:
    __engine = None
    __session = None

    def __init__(self):
        """Constructor of DBStorage class"""
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            user, pwd, host, db), pool_pre_ping=True)
        if env == 'test':
            Base.MetaData.drop_()

    def all(self, cls=None):
        """Returns a dictionary of objects"""
        _dict = {}
        if cls in self.__classes:
            res = DBStorage.__session.query(cls)
            for row in res:

