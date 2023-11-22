#!/usr/bin/Python3
"""This module defines the engine for the MySQL database"""

from models.base_model import BaseModel, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv


class DBStorage:
    """Database storage engine for HBNB project"""

    __engine = None  # Database engine
    __session = None  # Database session

    def __init__(self):
        """Initialize the database engine and session"""
        user = getenv('HBNB_MYSQL_USER')
        pwd = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        db = getenv('HBNB_MYSQL_DB')
        env = getenv('HBNB_ENV')

        # Create the MySQL database engine
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(user, pwd, host, db),
                                      pool_pre_ping=True)

        # Drop all tables if the environment is set to test
        if env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query and retrieve objects from the database"""
        my_dict = {}
        if cls is None:
            # Query all types of objects (User, State, City, Amenity, Place, and Review)
            for cl in Base.__subclasses__():
                result = DBStorage.__session.query(cl)
                for row in result:
                    key = "{}.{}".format(row.__class__.__name__, row.id)
                    my_dict[key] = row
        else:
            # Query objects based on the provided class
            result = DBStorage.__session.query(cls)
            for row in result:
                key = "{}.{}".format(row.__class__.__name__, row.id)
                my_dict[key] = row
        return my_dict

    def new(self, obj):
        """Add a new object to the current database session"""
        DBStorage.__session.add(obj)

    def save(self):
        """Commit all changes to the current database session"""
        DBStorage.__session.commit()

    def delete(self, obj=None):
        """Delete an object from the current database session"""
        if obj:
            DBStorage.__session.delete(obj)

    def reload(self):
        """Create the current database session and tables"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        DBStorage.__session = Session()

    def close(self):
        """Close the current database session"""
        DBStorage.__session.close()

