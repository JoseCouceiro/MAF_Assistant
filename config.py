from importlib import resources
import json
import os

def cfg_item(*items):
    data = Config.instance().data
    for key in items:
        data = data[key]
    return data

class SaveAndLoad():

    def __init__(self):
        self.config_json_path = os.path.join("resources", "config", "config.json")
    
    def load_config_file(self, file_path):
        with open(file_path, 'r') as __f:
            __data = json.load(__f)
        return __data
    
    def save_config_file(self, data, file_path):
        with open(file_path, 'w') as __f:
            json.dump(data, __f, indent=4)
        print('data dump')

class Config:

    __instance = None
    __config_json_path, __config_json_filename = "resources.config", "config.json"  
    

    @staticmethod
    def instance():
        if Config.__instance is None:
            Config()
        return Config.__instance

    def __init__(self):
        """ if Config.__instance is None: """
        Config.__instance = self

        with resources.path(Config.__config_json_path, Config.__config_json_filename) as json_file:
            with open(json_file) as file:
                self.data = json.load(file)
        """ else:
            raise Exception('Config Only Can Be Instancianted Once!!!') """
        
