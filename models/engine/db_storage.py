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
    """Defines the class DBStorage"""
    __engine = None
    __session = None
    __classes = [State, City, User, Place, Review, Amenity]

    def __init__(self):
        """Constructor of DBStorage class"""
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            user, pwd, host, db), pool_pre_ping=True)
        if env == 'test':
            Base.MetaData.drop_all()

    def all(self, cls=None):
        """Returns a dictionary of objects"""
        _dict = {}
        if cls in self.__classes:
            res = DBStorage.__session.query(cls)
            for row in res:
                key = '{}.{}'.format(row.__class__.__name__, row.id)
                _dict[key] = row
        elif cls is None:
            for cl in self.__classes:
                res = DBStorage.__session.query(cl)
                for row in res:
                    key = '{}.{}'.format(row.__class__.__name__, row.id)
                    _dict[key] = row
        return _dict

    def new(self, obj):
        """Adds a new object to the current database"""
        DBStorage.__session.add(obj)

    def save(self):
        """Commits all changes to the current database"""
        DBStorage.__session.commit()

    def delete(self, obj=None):
        """Deletes a new object added to database"""
        DBStorage.__session.delete(obj)

    def reload(self):
        """Create the current database session"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        DBStorage.__session = Session()

    def close(self):
        """Calls remove method"""
        DBStorage.__session.close()
