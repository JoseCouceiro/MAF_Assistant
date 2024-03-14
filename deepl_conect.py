import deepl
from config import Config
from config import cfg_item

class Translate:

    def __init__(self):

        #self.__configurator = Config()
        self.__auth_key = cfg_item('keys', 'deepl')
        self.__translator = deepl.Translator(self.__auth_key)
        
    def translate_to_sp(self, sentence):
        __sentence_sp = self.__translator.translate_text(sentence, target_lang = "ES")

        return __sentence_sp
