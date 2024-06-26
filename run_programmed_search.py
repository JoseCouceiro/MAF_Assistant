from config import Config
from config import cfg_item
from config import SaveAndLoad
from config import DataBase
from search_pubmed import Search

__configurations = Config()
__configurations.instance()
__saveandload = SaveAndLoad()
__database = DataBase()

__query_list = cfg_item('search_terms')
#__query_list = ["macitentan", "selexipag", "ambrisentan"]

__searcher = Search()

#__programmed_search_on = __searcher.run_programmed_search()
__programmed_search_on = True

while __programmed_search_on:
    __results_dic = dict()
    __already_found = list()
    for __query in __query_list:
        __selected, __rejected, __n_found = __searcher.run_search(__query, is_programmed=True)
        __selected_clean, __already_found = __searcher.remove_duplicates(__selected, __already_found)
        print(f'{len(__selected)} selected out of {__n_found} found')
        __selected_dics = __searcher.transform_article_list(__selected_clean) 
        __rejected_dics = __searcher.transform_article_list(__rejected)
        __total_n_dics = len(__rejected_dics)+len(__selected_dics)
        
        __results_dic[__query] = (__selected_dics, __total_n_dics)

        __database.save_to_database(__selected_dics)  
        __database.save_to_database(__rejected_dics)
        print('Database updated')
    
    __saveandload.save_history_file(__results_dic)
        
    print('Search Done')
    __programmed_search_on = False
