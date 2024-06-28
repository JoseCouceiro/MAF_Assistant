import json
from sqlalchemy import create_engine, Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from config import cfg_item

# Set up database connection
database_data = cfg_item("database")
db_host = database_data['host']
db_name = database_data['name']
db_user = database_data['user']
db_password = database_data['password']
db_port_number = database_data['port_number']
db_uri = f'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port_number}/{db_name}'
engine = create_engine(db_uri)
Base= declarative_base()

class Database():
    """
    This class represents a database manager for storing and retrieving configuration parameters.'
    This class initializes with configuration data retrieved from 'cfg_item()'. It provides access to parameters
    such as selection parameters, search terms, and countries list through the 'params_dic' attribute.
    """
    def __init__(self):
        self.__config_data = cfg_item()
        self.params_dic = {
            'selection_parameters': self.__config_data['selection_parameters'],
            'search_terms': self.__config_data['search_terms'],
            'countries_list': self.__config_data['countries_list']
            }

# Define database schema
class UserParams(Base):
    """
    This class maps to the 'user_params' table in the database. It includes columns for user ID ('user_id'),
    parameters ('parameters'), and saved searches ('saved_searches').
    """
    __tablename__ = 'user_params'
    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    parameters = Column(JSON)
    saved_searches = Column(JSON)

    def __init__(self, user_id, parameters):
        self.user_id = user_id
        self.parameters = parameters

# Create tables
Base.metadata.create_all(engine)

# Function to save parameters
def save_params(user_id, params):
    """
    Saves user parameters into the database or updates existing parameters if the user already exists.
    This function establishes a database session, serializes the 'params' dictionary into a JSON string,
    and performs either an update or insert operation into the 'user_params' table based on whether the
    user with 'user_id' already exists.
    Parameters:
        user_id : str
            The unique identifier for the user whose parameters are being saved or updated.
        params : dict
            A dictionary containing user-specific parameters to be stored in the database.
    Raises:
        SQLAlchemyError
            If there is an error with SQLAlchemy operations (e.g., database connection issues, query errors).
        json.JSONDecodeError
            If there is an error during JSON serialization of the 'params' dictionary.

    """
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        # Serialize the params dictionary to a JSON string
        if params:
            params_json = json.dumps(params)
        else:
            params_json = None
        # Check if user exists in the database
        user_params = session.query(UserParams).filter_by(user_id=user_id).first()
        if user_params:
            # Update params if user exists
            user_params.parameters = params_json
        else:
            # Create new entry if user doesn't exist
            user_params = UserParams(user_id=user_id, parameters=params_json)
            session.add(user_params)
        session.commit()
    except (SQLAlchemyError, json.JSONDecodeError) as e:
        session.rollback()
        raise e
    finally:
        session.close()

def save_searches(user_id, searches):
    """
    Saves user's saved searches into the database or updates existing saved searches if the user already exists.
    This function establishes a database session, serializes the 'searches' dictionary into a JSON string,
    and performs either an update or insert operation into the 'user_params' table based on whether the
    user with 'user_id' already exists.
    Parameters:
        user_id : str
            The unique identifier for the user whose saved searches are being saved or updated.
        searches : dict
            A dictionary containing user's saved search configurations to be stored in the database.
    Raises:
        SQLAlchemyError
            If there is an error with SQLAlchemy operations (e.g., database connection issues, query errors).
        json.JSONDecodeError
            If there is an error during JSON serialization of the 'searches' dictionary.
    """
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        # Serialize the searches dictionary to a JSON string
        if searches:
            searches_json = json.dumps(searches, ensure_ascii=True)
        else:
            searches_json = None
        # Check if user exists in the database
        user_params = session.query(UserParams).filter_by(user_id=user_id).first()
        if user_params:
            # Update searches if user exists
            user_params.saved_searches = searches_json
        else:
            # Create new entry if user doesn't exist
            user_params = UserParams(user_id=user_id, saved_searches=searches_json)
            session.add(user_params)
        session.commit()
    except (SQLAlchemyError, json.JSONDecodeError) as e:
        session.rollback()
        raise e
    finally:
        session.close()

# Function to retrieve parameters
def get_params(user_id):
    """
    Retrieves user parameters from the database based on the provided user_id.
    This function establishes a database session, queries the 'user_params' table for the user with
    the specified 'user_id', and retrieves the parameters stored as a JSON string. It deserializes
    the JSON string back into a dictionary format and returns it.
    Parameters:
        user_id: str
            The unique identifier for the user whose parameters are being retrieved.
    Returns:
        dict or None
            A dictionary containing user-specific parameters if found in the database, or None if no
            parameters are found or if there is an error during database retrieval.
    Raises:
        SQLAlchemyError
            If there is an error with SQLAlchemy operations (e.g., database connection issues, query errors).
        json.JSONDecodeError
            If there is an error during JSON deserialization of the parameters stored in the database.

    """
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        user_params = session.query(UserParams).filter_by(user_id=user_id).first()
        if user_params:
            if user_params.parameters:
            # Deserialize the JSON string back into a dictionary
                parameters = json.loads(user_params.parameters)
                return parameters
            else:
                return None
        else:
            return None
    except (SQLAlchemyError, json.JSONDecodeError) as e:
        raise e
    finally:
        session.close()

def get_searches(user_id):
    """
    Retrieves user's saved searches from the database based on the provided user_id.
    This function establishes a database session, queries the 'user_params' table for the user with
    the specified 'user_id', and retrieves the saved searches stored as a JSON string. It deserializes
    the JSON string back into a dictionary format and returns it.
    Parameters:
        user_id : str
            The unique identifier for the user whose saved searches are being retrieved.
    Returns:
        dict or None
            A dictionary containing user's saved searches if found in the database,
            or None if no saved searches are found or if there is an error during database retrieval.
    Raises:
        SQLAlchemyError
            If there is an error with SQLAlchemy operations (e.g., database connection issues, query errors).
        json.JSONDecodeError
            If there is an error during JSON deserialization of the saved searches stored in the database.

    """
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        user_params = session.query(UserParams).filter_by(user_id=user_id).first()
        if user_params:
            # Deserialize the JSON string back into a dictionary
            if user_params.saved_searches:
                searches = json.loads(user_params.saved_searches)
                return searches
            else:
                return None
        else:
            return None
    except (SQLAlchemyError, json.JSONDecodeError) as e:
        raise e
    finally:
        session.close()
    

    


        