#!/usr/bin/python3
""" Holds City class """

import models
from models.base_model import BaseModel, Base
from os import getenv
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

class City(BaseModel, Base):
    """Representation of City"""
    __tablename__ = 'cities'

    name = Column(String(128), nullable=False)
    state_id = Column(String(60), ForeignKey('states.id'), nullable=False)

    places = relationship("Place", backref="cities", cascade="all, delete-orphan")

    if getenv('HBNB_TYPE_STORAGE') != 'db':
        name = ""
        state_id = ""

    def __init__(self, *args, **kwargs):
        """Initializes City"""
        super().__init__(*args, **kwargs)

