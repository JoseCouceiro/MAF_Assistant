from metapub import PubMedFetcher
from metapub import FindIt
from parameters import Parameters
from classify_articles import Classify
from config import SaveAndLoad

class Search:

    def __init__(self):
        self.__params = Parameters()
        self.__fetcher = PubMedFetcher()
        self.__classifier = Classify()
        self.__saveandload = SaveAndLoad()
        self.__config_data = self.__saveandload.load_config_file()
        
    def __search_pubmed(self, query):
        pmids = self.__fetcher.pmids_for_query(
            f'({query}[Title/Abstract]) AND ("{self.__params.start_date_str}"[Date - Publication] : "{self.__params.end_date_str}"[Date - Publication])')
        print(f'({query}[Title/Abstract]) AND ("{self.__params.start_date_str}"[Date - Publication] : "{self.__params.end_date_str}"[Date - Publication])')
        return pmids

    def __fetch_articles(self, pmids_list, query, is_programmed):
        __selected = list()
        __rejected = list()
        for pmid in pmids_list:
            __article = self.__fetcher.article_by_pmid(int(pmid))
            __pass, __score =  self.__classifier.rater(__article, query)
            if __pass:
                __selected.append((__article, __score, __pass))
            if not __pass:
                __rejected.append((__article, __score, __pass))
        __selected_ordered = sorted(__selected, key = lambda x: x[1], reverse=True)
        if is_programmed:
            return __selected, __rejected
        if not is_programmed:
            return __selected_ordered
    
    def transform_article_list(self, art_list):
        transformed_art_list = list()
        for __tup in art_list:
            __art_dic = dict()
            __art, __score, __pass = __tup
            __art_dic['title'] = __art.title
            __art_dic['authors_str'] = __art.authors_str
            __art_dic['doi'] = __art.doi
            __art_dic['abstract'] = __art.abstract
            __art_dic['pmid'] = __art.pmid
            __art_dic['score'] = __score
            __art_dic['selected'] = __pass
            transformed_art_list.append(__art_dic)
        return transformed_art_list

    def run_search(self, query, is_programmed):
        print(query)
        __pmids = self.__search_pubmed(query)
        __n_found = len(__pmids)
        print('Number of articles found: ', len(__pmids))
        __selected, __rejected = self.__fetch_articles(__pmids, query, is_programmed)
        if not is_programmed:
            return __selected, __n_found
        if is_programmed:
            return __selected, __rejected, __n_found
         
    def __is_searching_day(self):
        if self.__params.day_week == self.__config_data['programmed_search']['day_of_search']:
            return True
        
    def __reset_programmed_search(self):
        self.__config_data['programmed_search']['programmed_search_done'] = False
        self.__saveandload.save_config_file(self.__config_data)
        
    def run_programmed_search(self):
        if self.__is_searching_day():
            print("It's searching day")
            if self.__config_data['programmed_search']['programmed_search_done'] == False:
                self.__config_data['programmed_search']['programmed_search_done'] = True
                self.__saveandload.save_config_file(self.__config_data)
                return True
            else:
                print('The programmed search has already been done')
        else:
            print("Not a searching day")
            self.__reset_programmed_search()
    
    
            



    

