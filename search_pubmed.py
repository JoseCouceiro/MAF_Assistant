from metapub import PubMedFetcher
from metapub import FindIt
import streamlit as st
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
        
    def __search_pubmed(self, query, start_date, end_date):
        pmids = self.__fetcher.pmids_for_query(
            f'({query}[Title/Abstract]) AND ("{start_date}"[Date - Publication] : "{end_date}"[Date - Publication])')
        print(f'({query}[Title/Abstract]) AND ("{start_date}"[Date - Publication] : "{end_date}"[Date - Publication])')
        return pmids

    def __fetch_articles(self, pmids_list, query, user, is_programmed):
        __selected = list()
        __rejected = list()
        for pmid in pmids_list:
            try:
                __article = self.__fetcher.article_by_pmid(int(pmid))
            except:
                st.error(f'Metapub exception: PMID {int(pmid)} not found')
            __pass, __score =  self.__classifier.rater(__article, query, user)
            if __pass:
                __selected.append((__article, __score, __pass))
            if not __pass:
                __rejected.append((__article, __score, __pass))
        __selected_ordered = sorted(__selected, key = lambda x: x[1], reverse=True)
        if is_programmed:
            return __selected, __rejected
        if not is_programmed:
            return __selected_ordered, __rejected
    
    def transform_article_list(self, art_list):
        transformed_art_list = list()
        for __tup in art_list:
            __art_dic = dict()
            __art, __score, __pass = __tup
            __art_dic['title'] = __art.title
            __art_dic['authors_str'] = __art.authors_str
            __art_dic['doi'] = __art.doi
            __art_dic['abstract'] = __art.abstract[0]
            __art_dic['pmid'] = __art.pmid
            __art_dic['score'] = __score
            __art_dic['selected'] = __pass
            __art_dic['translated'] = __art.abstract[1]
            transformed_art_list.append(__art_dic)
        return transformed_art_list

    def run_search(self, query, user, is_programmed, start_date, end_date):
        print(query)
        __pmids = self.__search_pubmed(query,  start_date, end_date)
        __n_found = len(__pmids)
        print('Number of articles found: ', len(__pmids))
        __selected, __rejected = self.__fetch_articles(__pmids, query, user, is_programmed)
        if not is_programmed:
            return __selected, __n_found
        if is_programmed:
            return __selected, __rejected, __n_found
        
    def remove_duplicates(self, selected_list, duplicates_list):
        #st.write('already found from inside remove duplicates: ', duplicates_list)
        #st.write('input selected list: ', selected_list)
        #st.write('input duplicates_list: ', duplicates_list)
        if len(selected_list) != 0:
            for __tup in selected_list:
                __art, __score, __pass = __tup
                #st.write('searching duplicates')
                if __art.pmid in duplicates_list:
                    #st.write('selected list in if loop: ', selected_list)
                    selected_list.remove(__tup)
                    #st.write('selected list: ', selected_list)
                    #st.write(f'article {__art.pmid} in already found')
                else:
                    duplicates_list.append(__art.pmid)
                    #st.write(f'article {__art.pmid} not in already found')
                    #st.write('selected list: ', selected_list)
        return selected_list, duplicates_list
         
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
    
    
            



    

