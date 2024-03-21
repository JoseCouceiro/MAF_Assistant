import json
import os
import csv
from importlib import resources
import pandas as pd
from parameters import Parameters

def cfg_item(*items):
    data = Config.instance().data
    for key in items:
        data = data[key]
    return data

class SaveAndLoad:

    def __init__(self):
        self.__params = Parameters()
        self.__config_json_path = os.path.join("resources", "config", "config.json")
        self.__history_path = os.path.join("resources", "saved_searches", self.__params.today_str+'.json')

    def load_config_file(self):
        with open(self.__config_json_path, 'r') as __f:
            __data = json.load(__f)
        return __data
    
    def save_config_file(self, data):
        with open(self.__config_json_path, 'w') as __f:
            json.dump(data, __f, indent=4)
        print('Config file saved')

    def save_history_file(self, data):
        with open(self.__history_path, 'w') as __f:
            json.dump(data, __f)
        print('New history file saved')

class DataBase:

    def __init__(self):
        self.__database_path = os.path.join("resources", "database", 'database.csv')
        self.__fieldnames = ['title','authors_str','doi','abstract','pmid','score','selected']
    
    def save_to_database(self, lst):
        __csv_file = open(self.__database_path, 'a', newline='', encoding='utf-8')
        __writer = csv.DictWriter(__csv_file, self.__fieldnames)
        for __dic in lst:
            __writer.writerow(__dic)
        __csv_file.close()
    
    def clean_dataframe(self, df):
        df.drop(subset=['doi'], inplace = True)
        return df

class Config:

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