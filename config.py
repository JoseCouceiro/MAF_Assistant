import json
import os
from importlib import resources
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
            __f.write(data)
        print('New history file saved')

class Article:

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)

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