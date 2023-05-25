#!/usr/bin/python3
""" State Module for HBNB project"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from models.city import City
import models


class State(BaseModel, Base):
    """ State class """
    if models.storage_type == 'db':
        __tablename__ = "states"
        name = Column(String(128), nullable=False)
        cities = relationship('City', backref='state')
    else:
        name = ''
    if models.storage_type != 'db':
        @property
        def cities(self):
            """Getter attribute cities that returns the list of Cities"""
            related_cities = []
            cities = models.storage.all(City)
            for city in cities.values():
                if self.id == city.state_id:
                    related_cities.append(city)
            return related_cities
