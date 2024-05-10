from datetime import datetime, timedelta
from config import SaveAndLoad

class Parameters:
    def __init__(self):
        self.__config = SaveAndLoad()
        self.__config_data = self.__config.load_config_file()
        # date
        self.__end_date = datetime.now()
        self.__start_date = self.__end_date - timedelta(days=self.__config_data['programmed_search']['search_span'])
        #self.start_date_str = self.__start_date.strftime('%Y/%m/%d')
        #self.end_date_str = self.__end_date.strftime('%Y/%m/%d')
        #self.today_str = self.__end_date.strftime('%Y_%m_%d')
        self.day_week = datetime.weekday(self.__end_date)
        
        # fixed dates
        self.start_date_str = '2024/04/22'
        self.end_date_str = '2024/05/29'
        self.today_str = '2024_05_29'


        
    
        