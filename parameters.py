from datetime import datetime, timedelta


class Parameters:
    def __init__(self):
        # date
        self.__end_date = datetime.now()
        self.__start_date = self.__end_date - timedelta(days=7)
        self.start_date_str = self.__start_date.strftime('%Y/%m/%d')
        self.end_date_str = self.__end_date.strftime('%Y/%m/%d')
        self.today_str = self.__end_date.strftime('%Y_%m_%d')
        self.day_week = datetime.weekday(self.__end_date)
        
        # fixed dates
        #self.start_date_str = '2024/04/22'
        #self.end_date_str = '2024/04/29'
        #self.today_str = '2024_04_29'
    

        
        
        
    
        