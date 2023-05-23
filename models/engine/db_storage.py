#!/usr/bin/python3
"""Defines the engine for MySQL database"""
from models.base_model import BaseModel, Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from sqlalchemy import (create_engine)
from sqlalchemy.orm import sessionmaker, scoped_session
import os


user = os.getenv('HBNB_MYSQL_USER')
pwd = os.getenv('HBNB_MYSQL_PWD')
host = os.getenv('HBNB_MYSQL_HOST')
db = os.getenv('HBNB_MYSQL_DB')
env = os.getenv('HBNB_ENV')


classes = {
        "User": User,
        "Place": Place,
        "State": State,
        "City": City,
        "Amenity": Amenity,
        "Review": Review,
}


class DBStorage:
    """Defines the class DBStorage"""
    __engine = None
    __session = None

    def __init__(self):
        """Constructor of DBStorage class"""
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            user, pwd, host, db), pool_pre_ping=True)
        if env == 'test':
            Base.metadata.drop_all()

    def all(self, cls=None):
        """Returns a dictionary of objects"""
        all_objs = {}
        for cl in classes:
            if not cls or cls is classes[cl]:
                for obj in self.__session.query(classes[cl]).all():
                    key = '{}.{}'.format(obj.__class__.__name__, obj.id)
                    all_objs[key] = obj
        return all_objs

    def new(self, obj):
        """Adds a new object to the current database"""
        self.__session.add(obj)

    def save(self):
        """Commits all changes to the current database"""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes a new object added to database"""
        self.__session.delete(obj)

    def reload(self):
        """Create the current database session"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        self.__session = scoped_session(session_factory)

    def close(self):
        """Calls remove method"""
        self.__session.close()
