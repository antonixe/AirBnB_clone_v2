#!/usr/bin/python3
""" Holds class User """
import models
from models.base_model import BaseModel, Base
from os import getenv
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String
from werkzeug.security import generate_password_hash, check_password_hash


class User(BaseModel, Base):
    """Representation of a user """
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        __tablename__ = 'users'
        email = Column(String(128),
                       nullable=False)
        password_hash = Column(String(128),
                               nullable=False)
        first_name = Column(String(128),
                            nullable=True)
        last_name = Column(String(128),
                           nullable=True)
        places = relationship("Place",
                              backref="user",
                              cascade="all, delete-orphan")
        reviews = relationship("Review",
                               backref="user",
                               cascade="all, delete-orphan")
    else:
        email = ""
        password_hash = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """Initializes user"""
        super().__init__(*args, **kwargs)

    @property
    def password(self) -> str:
        """Getter for the password"""
        return self.password_hash

    @password.setter
    def password(self, value: str) -> None:
        """Setter for the password"""
        self.password_hash = generate_password_hash(value)

    def check_password(self, password: str) -> bool:
        """Check whether the given password matches the user's password"""
        return check_password_hash(self.password_hash, password)

    def __str__(self) -> str:
        """Returns a string representation of the User instance"""
        return f"[User] ({self.id}) {self.email}"

    def to_dict(self) -> dict:
        """Returns a dictionary representation of the User instance"""
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

