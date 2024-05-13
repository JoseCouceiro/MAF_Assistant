from config import Config
from config import cfg_item
from config import SaveAndLoad
from config import DataBase
from user_params import save_searches, get_searches, get_params
from search_pubmed import Search

__configurations = Config()
__configurations.instance()
__saveandload = SaveAndLoad()
__database = DataBase()

__date = "2024/05/13" #__saveandload.today_str

#__query_list = ['ambrisentan'] #["macitentan", "selexipag", "ambrisentan"]

__searcher = Search()

#__programmed_search_on = __searcher.run_programmed_search()
__programmed_search_on = True

while __programmed_search_on:
    __user = input('Introduce your username: ')
    __query_list = get_params(__user)['search_terms']
    if __user:
        print('Running search')
        __results_dic = dict()
        __already_found = list()
        for __query in __query_list:
            __selected, __rejected, __n_found = __searcher.run_search(__query, __user, is_programmed=True)
            __selected_clean, __already_found = __searcher.remove_duplicates(__selected, __already_found)
            print(f'{len(__selected)} selected out of {__n_found} found')
            __selected_dics = __searcher.transform_article_list(__selected_clean) 
            __rejected_dics = __searcher.transform_article_list(__rejected)
            
            __results_dic[__query] = __selected_dics

            __database.save_to_database(__selected_dics)  
            __database.save_to_database(__rejected_dics)
            print('Database updated')
        
        __save_searches_dic = get_searches(__user)
        if __save_searches_dic:
            __save_searches_dic[__date] = __results_dic
        else:
            __save_searches_dic = dict()
            __save_searches_dic[__date] = __results_dic
        save_searches(__user, __save_searches_dic)
            
        print('Search Done')
        __programmed_search_on = False
