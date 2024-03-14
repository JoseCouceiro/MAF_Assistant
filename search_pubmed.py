from metapub import PubMedFetcher
from metapub import FindIt
from parameters import Parameters
from classify_articles import Classify


class Search:

    def __init__(self):
        self.__params = Parameters()
        self.__fetcher = PubMedFetcher()
        self.__classifier = Classify()
        
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
    
    def is_searching_day(self):
        if self.__params.day_week == 2:
            return True


    

