import json
import os
import csv
from importlib import resources
from datetime import datetime

def cfg_item(*items):
    data = Config.instance().data
    for key in items:
        data = data[key]
    return data

class SaveAndLoad:
    """
    This class contains the functions that save and load the config file
    """
    def __init__(self):
        self.__today = datetime.now()
        self.today_str = self.__today.strftime('%Y_%m_%d')
        self.__config_json_path = os.path.join("resources", "config", "config.json")
    
    def load_config_file(self):
        """
        Function that opens the config file as a json and returns the data contained in it as a dictionary
        """
        with open(self.__config_json_path, 'r') as __f:
            __data = json.load(__f)
        return __data
    
    def save_config_file(self, data):
        """
        This function takes a dictionary and saves the data contained in it into the config file in json format 
        """
        with open(self.__config_json_path, 'w') as __f:
            json.dump(data, __f, indent=4)
        print('Config file saved')

class DataBase:
    """
    Class that saves the search results into a csv file. This class was written for app development puposes only
    """
    def __init__(self):
        self.__database_path = os.path.join("resources", "database", 'database.csv')
        self.__fieldnames = ['title','authors_str','doi','abstract','pmid','score','selected']
    
    def save_to_database(self, lst):
        """
        Function that takes a list of dictionaries and saves the data contained in those dictionaries into a csv file
        """
        __csv_file = open(self.__database_path, 'a', newline='', encoding='utf-8')
        __writer = csv.DictWriter(__csv_file, self.__fieldnames)
        for __dic in lst:
            __writer.writerow(__dic)
        __csv_file.close()
    
class Config:
    """
    This class generates an instance that allows loading data from the config file
    """
    __instance = None
    __config_json_path, __config_json_filename = "resources.config", "config.json"  
    
    @staticmethod
    def instance():
        if Config.__instance is None:
            Config()
        return Config.__instance

    def __init__(self):
        Config.__instance = self
        with resources.path(Config.__config_json_path, Config.__config_json_filename) as json_file:
            with open(json_file) as file:
                self.data = json.load(file)