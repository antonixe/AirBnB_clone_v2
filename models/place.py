#!/usr/bin/python3
""" holds class Place"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, Integer, Float, Table, ForeignKey
from sqlalchemy.orm import relationship

if getenv('HBNB_TYPE_STORAGE') == 'db':
    place_amenity = Table('place_amenity', Base.metadata,
                          Column('place_id',
                                 String(60),
                                 ForeignKey('places.id'),
                                 primary_key=True,
                                 nullable=False),
                          Column('amenity_id',
                                 String(60),
                                 ForeignKey('amenities.id'),
                                 primary_key=True,
                                 nullable=False))


class Place(BaseModel, Base):
    """Representation of Place"""
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        __tablename__ = 'places'
        city_id = Column(String(60),
                         ForeignKey("cities.id"),
                         nullable=False)
        user_id = Column(String(60),
                         ForeignKey('users.id'),
                         nullable=False)
        name = Column(String(128),
                      nullable=False)
        description = Column(String(1024),
                             nullable=True)
        number_rooms = Column(Integer,
                              default=0,
                              nullable=False)
        number_bathrooms = Column(Integer,
                                  default=0,
                                  nullable=False)
        max_guest = Column(Integer,
                           default=0,
                           nullable=False)
        price_by_night = Column(Integer,
                                default=0,
                                nullable=False)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        reviews = relationship("Review", cascade="all, delete",
                               backref="places")
        amenities = relationship("Amenity",
                                 secondary='place_amenity',
                                 viewonly=False,
                                 backref="place_amenities")
    else:
        city_id = user_id = name = description = ""
        number_rooms = number_bathrooms = max_guest = price_by_night = 0
        latitude = longitude = 0.0
        amenity_ids = []

    def __init__(self, *args, **kwargs):
        """initializes Place"""
        super().__init__(*args, **kwargs)

    @property
    def reviews(self):
        """Returns the list of Review instances"""
        reviews = [review for review in models.storage.all("Review").values()
                   if review.place_id == self.id]
        return reviews

    if getenv('HBNB_TYPE_STORAGE') != 'db':
        @property
        def amenities(self):
            """Returns the list of Amenity instances"""
            amenities = [amenity for amenity in models.storage.all("Amenity").values()
                         if amenity.place_id == self.id]
            return amenities

