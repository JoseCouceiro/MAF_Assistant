from datetime import datetime, timedelta
from sqlalchemy import create_engine, Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import SaveAndLoad


class Parameters:
    def __init__(self):
        self.__config = SaveAndLoad()
        self.__config_data = self.__config.load_config_file()
        # date
        self.__end_date = datetime.now()
        self.__start_date = self.__end_date - timedelta(days=self.__config_data['programmed_search']['search_span'])
        self.start_date_str = self.__start_date.strftime('%Y/%m/%d')
        self.end_date_str = self.__end_date.strftime('%Y/%m/%d')
        self.today_str = self.__end_date.strftime('%Y_%m_%d')
        self.day_week = datetime.weekday(self.__end_date)
        
        # fixed dates
        #self.start_date_str = '2024/04/15'
        #self.end_date_str = '2024/04/22'
        #self.today_str = '2024_04_22'

# Define database schema
class UserParams():

    def __init__(self):
        # Set up database connection
        self.engine = create_engine('sqlite:///user_params.db')
        self.Base = declarative_base()

        self.__tablename__ = 'user_params'
        self.id = Column(Integer, primary_key=True)
        self.user_id = Column(String)
        self.parameters = Column(JSON)

    # Create tables
        self.Base.metadata.create_all(self.engine)

# Function to save parameters
    def save_params(self, user_id, params):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        user_params = self.Base(user_id=user_id, parameters=params)
        session.add(user_params)
        session.commit()
        session.close()

    # Function to retrieve parameters
    def get_params(self, user_id):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        user_params = session.query(self.Base).filter_by(user_id=user_id).first()
        session.close()
        if user_params:
            return user_params.parameters
        else:
            return None

    
    """ # Usage
    user_id = 'user123'
    params = {'param1': value1, 'param2': value2}
    save_params(user_id, params)
    retrieved_params = get_params(user_id) """
        
        
        
    
        