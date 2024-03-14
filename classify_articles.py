from config import cfg_item

class Classify():

    def __from_countries_func(self, aff_set):
        for __country in aff_set:
            if __country in cfg_item('countries_list'):
                return True
        return False

    def __made_in_spain_func(self, aff_set):
        return True if 'spain' in aff_set else False

    def __query_in_title_func(self, art, query):
        return True if query.lower() in art.title.lower() else False

    def __is_rct_func(self, art):
        if art.abstract != None:
            __there_is_rct = 'rct' in art.abstract.lower()
            __there_is_research = 'research clinical trial' in art.abstract.lower()
            return True if (__there_is_rct or __there_is_research) else False
        
    def __is_meta_analysis_func(self, art):
        if art.abstract != None:
            __in_abstract = 'meta-analyis' in art.abstract.lower() 
            __in_title = 'meta-analyis' in art.title.lower()
            return True if (__in_abstract or __in_title) else False
        
    def __get_affiliations(self, art):
        __article_dic = art.to_dict()
        __affiliations_set = set()
        for __auth in __article_dic['author_list']:
            if len(__auth.affiliations) != 0:
                __affiliations_set.add(__auth.affiliations[0].split()[-1].strip('.').lower())
        return __affiliations_set
        
    def rater(self, art, query):
        __affiliations_set = self.__get_affiliations(art)
        __score = 0
        print('article: ', art)
        __thresh = cfg_item('selection_parameters', 'threshold')
        if self.__query_in_title_func(art, query):
            __score = cfg_item('selection_parameters', 'query_in_title')
        if self.__from_countries_func(__affiliations_set):
            __score += cfg_item('selection_parameters', 'from_countries')
        if self.__is_rct_func(art):
            __score += cfg_item('selection_parameters', 'is_rct')
            print('is_rct', __score)
        if self.__made_in_spain_func(__affiliations_set):
            __score += cfg_item('selection_parameters', 'made_in_spain')
            print('made_in_spain', __score)
        if self.__is_meta_analysis_func(art):
            __score += cfg_item('selection_parameters', 'is_meta_analysis')
            print('is_meta_analysis', __score)
        print('Article score: ', __score)
        print('Threshold: ', __thresh)
        print('Selected: ', __score >= __thresh)
        __pass = __score >= __thresh
        return __pass, __score