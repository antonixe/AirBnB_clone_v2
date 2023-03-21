from os import environ
from models.base_model import Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
""" import the necessary modules and classes"""


class DBStorage:
    """class defination"""
    __engine = None
    __session = None

    def __init__(self):
        """initializes the DBStorage object"""
        user = environ.get("HBNB_MYSQL_USER")
        password = environ.get("HBNB_MYSQL_PWD")
        host = environ.get("HBNB_MYSQL_HOST", "localhost")
        db = environ.get("HBNB_MYSQL_DB")

        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}:3306/{}'.
            format(user, password, host, db),
            pool_pre_ping=True)

        if environ.get("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ returns a dictionary containing all objects \
                of a given class, or all objects if no class is specified"""
        classes = [User, State, City, Amenity, Place, Review]

        if cls is not None and cls in classes:
            classes = [cls]

        objects = {}

        for c in classes:
            for obj in self.__session.query(c):
                key = "{}.{}".format(type(obj).__name__, obj.id)
                objects[key] = obj

        return objects

    def new(self, obj):
        """adds an object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commits all changes made to the current\
                database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """deletes an object from the current database session"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """recreates the database session and creates\
                all the tables in the database"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
                bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session_factory)()
