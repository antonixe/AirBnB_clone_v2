#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    cities = relationship("city", cascade="all, delete-orphan", backref="state")

    @property
    def cities(self):
        """getter attribute that returns the list of city instances with state_id equals to the current State.id"""
        city_list = []
        for city in models.storage.all("city").values():
            if city.state_id == self.id:
                city_list.append(city)
        return city_list
