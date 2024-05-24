import json
from sqlalchemy import create_engine, Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from config import cfg_item

# Set up database connection
db_uri = 'mysql+pymysql://sql7708417:VtxITqbq6b@sql7.freesqldatabase.com:3306/sql7708417'
engine = create_engine(db_uri)
Base= declarative_base()

class Database():
    def __init__(self):
        self.__config_data = cfg_item()
        self.params_dic = {
            'selection_parameters': self.__config_data['selection_parameters'],
            'search_terms': self.__config_data['search_terms'],
            'countries_list': self.__config_data['countries_list']
            }

# Define database schema
class UserParams(Base):
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
""" def save_params(user_id, params):
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Check if user exists in the database
    user_params = session.query(UserParams).filter_by(user_id=user_id).first()
    if user_params:
        # Update parameters if user exists
        user_params.parameters = params
    else:
        # Create new entry if user doesn't exist
        user_params = UserParams(user_id=user_id, parameters=params)
        session.add(user_params)
    
    session.commit()
    session.close() """

def save_params(user_id, params):
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Serialize the params dictionary to a JSON string
        params_json = json.dumps(params)
        
        # Check if user exists in the database
        user_params = session.query(UserParams).filter_by(user_id=user_id).first()
        if user_params:
            # Update params if user exists
            if user_params.parameters:
                user_params.parameters = params_json
            else:
                params_json = None
        else:
            # Create new entry if user doesn't exist
            user_params = UserParams(user_id=user_id, saved_params=params_json)
            session.add(user_params)
        
        session.commit()
    except (SQLAlchemyError, json.JSONDecodeError) as e:
        session.rollback()
        raise e
    finally:
        session.close()

""" def save_searches(user_id, searches):
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Check if user exists in the database
    user_params = session.query(UserParams).filter_by(user_id=user_id).first()
    if user_params:
        # Update searches if user exists
        user_params.saved_searches = searches
    else:
        # Create new entry if user doesn't exist
        user_params = UserParams(user_id=user_id, parameters=searches)
        session.add(user_params)
    
    session.commit()
    session.close() """

def save_searches(user_id, searches):
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Serialize the searches dictionary to a JSON string
        searches_json = json.dumps(searches)
        
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
""" def get_params(user_id):
    Session = sessionmaker(bind= engine)
    session = Session()
    user_params = session.query(UserParams).filter_by(user_id=user_id).first()
    session.close()
    if user_params:
        return user_params.parameters
    else:
        return None """

def get_params(user_id):
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        user_params = session.query(UserParams).filter_by(user_id=user_id).first()
        if user_params:
            # Deserialize the JSON string back into a dictionary
            if user_params.parameters:
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


""" def get_searches(user_id):
    Session = sessionmaker(bind= engine)
    session = Session()
    user_params = session.query(UserParams).filter_by(user_id=user_id).first()
    session.close()
    if user_params:
        return user_params.saved_searches
    else:
        return None """

def get_searches(user_id):
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
    

    


        