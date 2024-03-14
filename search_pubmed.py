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

    def __fetch_articles(self, pmids_list, query):
        __selected = list()
        for pmid in pmids_list:
            __article = self.__fetcher.article_by_pmid(int(pmid))
            __pass, __score =  self.__classifier.rater(__article, query)
            if __pass:
                __selected.append((__article, __score))
        __selected_ordered = sorted(__selected, key = lambda x: x[1], reverse=True)
        return __selected_ordered
    
    def run_search(self, query):
        print(query)
        __pmids = self.__search_pubmed(query)
        __n_found = len(__pmids)
        print('Number of articles found: ', len(__pmids))
        __selected = self.__fetch_articles(__pmids, query)
        return __selected, __n_found
    
    def __is_searching_day(self):
        if self.__params.day_week == self.__config_data['programmed_search']['day_of_search']:
            return True
        
    def __reset_programmed_search(self):
        self.__config_data['programmed_search']['programmed_search_done'] = False
        self.__saveandload.save_config_file(self.__config_data)
        
    def run_programmed_search(self):
        if self.__is_searching_day():
            if self.__config_data['programmed_search']['programmed_search_done'] == False:
                self.__config_data['programmed_search']['programmed_search_done'] = True
                self.__saveandload.save_config_file(self.__config_data)
                return True
        else:
            self.__reset_programmed_search()
    
    
            



    

