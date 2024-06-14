import re
from config import cfg_item
from user_params import get_params

class Classify():
    """
    Class that contains all the functions necessary to rate articles and give them a final score
    """
    def __from_countries_func(self, aff_set):
        """
        Function that takes a set of countries, checks if any country in the set is also in the list of countries of interest and returns a boolean accordingly
        Input: a set
        Output: a boolean
        """
        for __country in aff_set:
            if __country in cfg_item('countries_list'):
                return True
        return False

    def __made_in_spain_func(self, aff_set):
        """
        Function that takes a set of countries, checks if 'Spain' is one of them and returns a boolean accordingly
        Input: a set
        Output: a boolean
        """
        return True if 'spain' in aff_set else False

    def __query_in_title_func(self, art, query):
        """
        This function takes an article object from deep_conect and a string, then checks if the string is in thte title of the article and returns a boolean accordingly
        Input: an article object and a string
        Output: a boolean
        """
        return True if query.lower() in art.title.lower() else False

    def __is_rct_func(self, art):
        """
        This function takes an article object from deep_conect, determines whether the string 'rct' or 'research clinical trial' are present in the abstract of the article and returns a boolean accordingly
        Input: an article object
        Ouput: a boolean
        """
        if art.abstract != None:
            __there_is_rct = 'rct' in art.abstract.lower()
            __there_is_research = 'research clinical trial' in art.abstract.lower()
            return True if (__there_is_rct or __there_is_research) else False
        
    def __is_meta_analysis_func(self, art):
        """
        This function takes an article object from deep_conect, determines whether the string 'meta-analyis' is present in either the title or the abstract of the article and returns a boolean accordingly
        Input: an article object
        Ouput: a boolean
        """
        if art.abstract != None:
            __in_abstract = 'meta-analyis' in art.abstract.lower() 
            __in_title = 'meta-analyis' in art.title.lower()
            return True if (__in_abstract or __in_title) else False
        
    def __get_affiliations(self, art):
        """
        This function takes an article object from deep_conect, determines whether the string 'meta-analyis' is present in either the title or the abstract of the article and returns a boolean accordingly
        Input: an article object
        Ouput: a boolean
        """
        __article_dic = art.to_dict()
        __affiliations_set = set()
        for __auth in __article_dic['author_list']:
            if len(__auth.affiliations) != 0:
                __affiliations_set.add(__auth.affiliations[0].split()[-1].strip('.').lower())
        return __affiliations_set
    
    def __is_in_vitro(self, art):
        """
        This function takes an article object from deep_conect, determines whether any of a series of words is present in the abstract of the article and returns a boolean accordingly
        Input: an article object
        Ouput: a boolean
        """
        __iv_words = ['dog', 'rat', 'in vitro', 'genomic', 'metabolomic']
        if art.abstract != None:
            for word in __iv_words:
                return True if re.search(r'\b'+word+'\b', art.abstract.lower()) else False
    
    def __is_case_report(self, art):
        """
        This function takes an article object from deep_conect, determines whether the string 'case report' is present in the title of the article and returns a boolean accordingly
        Input: an article object
        Ouput: a boolean
        """
        return True if 'case report' in art.title.lower() else False
    
    def __is_in_english(self, art):
        """
        This function takes an article object from deep_conect, determines whether the title of the article is between brackets and returns a boolean accordingly. \n
        The title being between brackets means the article language is not English
        Input: an article object
        Ouput: a boolean
        """
        pattern = r'^\[(.*?)\]\.'
        found = re.search(pattern, art.title)
        return False if found else True
        
    def rater(self, art, query, user):
        """
        This function takes an article object from deep_conect, a string and a username.
        The username is used to call the database and retrieve values for that particular user.
        The query and the article are passed to the different functions of the class.
        Each function returning true adds a value to a score. The value is determined in the database by the user.
        The final score is compared to the threshold set in the database by the user.
        If the score is higher than the threshold the function returns True, otherwise False.
        Input: an article object, a 'query' string, a 'username' string
        Ouput: a boolean
        """
        __user_params = get_params(user)['selection_parameters']
        __affiliations_set = self.__get_affiliations(art)
        __score = 0
        print('article: ', art)
        __thresh = __user_params['threshold']
        if self.__query_in_title_func(art, query):
            print('THE QUERY IS IN THE TITLE')
            __score = __user_params['query_in_title']
        if self.__from_countries_func(__affiliations_set):
            print('IT IS FROM COUNTRIES OF INTEREST')
            __score += __user_params['from_countries']
        if self.__is_rct_func(art):
            print('IT IS AN RCT')
            __score += __user_params['is_rct']
        if self.__made_in_spain_func(__affiliations_set):
            print('MADE IN SPAIN')
            __score += __user_params['made_in_spain']
        if self.__is_meta_analysis_func(art):
            print('IT IS META-ANALYSIS')
            __score += __user_params['is_meta_analysis']
        if not self.__made_in_spain_func(__affiliations_set):
            if self.__is_case_report(art):
                print('IT IS A CASE REPORT')
                __score += __user_params['is_case_report']
        if self.__is_in_vitro(art):
            print('IT IS IN VITRO')
            __score += __user_params['is_in_vitro']
        if not self.__is_in_english(art):
            print('IT IS NOT IN ENGLISH')
            __score += __user_params['not_in_english']
        print('Article score: ', __score)
        print('Threshold: ', __thresh)
        print('Selected: ', __score >= __thresh)
        __pass = __score >= __thresh
        return __pass, __score