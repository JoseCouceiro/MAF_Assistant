import deepl
from config import cfg_item

class Translate:
    """
    This class handles the conection with the translation service (DeepL).
    It also contains 'ad hoc' functions for the translation of article abstracts.
    """

    def __init__(self):
        self.__auth_key = cfg_item('keys', 'deepl')
        self.__translator = deepl.Translator(self.__auth_key)
        
    def __translate_to_sp(self, sentence):
        """
        Function that translates a given string from English to Spanish.
        Input: a string in English.
        Output: a string in Spanish.
        """
        __sentence_sp = self.__translator.translate_text(sentence, target_lang = "ES")

        return __sentence_sp
    
    def __translate_abstract(self, art_abstract):
        """
        This function takes an article abstract in English and translates it to Spanish using the function 'translate_to_sp'.
        Sometimes the abstract is null, so the function checks it to prevent errors in the function 'translate_to_sp'.
        In case the translation is productive, the function returns the translated abstract and True in a tuple, but it returns the original abstract and False in case the translation fails.
        Input: a string or null.
        Output: a tuple containing a string and a boolean.
        """
        if art_abstract != None:
            try:
                art_abstract_sp = self.__translate_to_sp(art_abstract)
                return art_abstract_sp, True
            except:
                return art_abstract, False
            
    def translate_selected(self, selected):
        """
        Function that translates the abstracts of selected articles.
        This method iterates over a list of selected articles, scores, and pass values. For each article, 
        it translates the abstract using the '__translate_abstract' method and updates the article's abstract.
        Input:
            selected (list of tuples): A list of tuples, where each tuple contains:
                - __art (object): An article object.
                - __score (float): A score associated with the article.
                - __pass (bool): A pass/fail indicator associated with the article.
        Output:
            list of tuples: The updated list of tuples with translated abstracts.
        """
        for __art, __score, __pass in selected:
            __art.abstract = self.__translate_abstract(__art.abstract)
        return selected
            

            
