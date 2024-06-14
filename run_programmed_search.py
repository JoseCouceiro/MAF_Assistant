from config import Config
from config import cfg_item
from config import SaveAndLoad
from config import DataBase
from deepl_conect import Translate
from user_params import save_searches, get_searches, get_params
from search_pubmed import Search

__configurations = Config()
__configurations.instance()
__saveandload = SaveAndLoad()
__database = DataBase()
__translator = Translate()


__searcher = Search()

__date = __saveandload.today_str
#__date = "2024/05/27"

__programmed_search_on = __searcher.run_programmed_search()
#__programmed_search_on = True

while __programmed_search_on:
    __user = input('Introduce your username: ')
    __query_list = get_params(__user)['search_terms']
    #__query_list = ["macitentan", "selexipag", "ambrisentan", "bosentan", "sotatercept", "riociguat"]
    #__query_list = ["Congenital heart disease AND pulmonary hypertension", "Cardiopulmonary exercise test AND pulmonary hypertension", "Systemic sclerosis AND pulmonary hypertension", "Connective tissue disease AND pulmonary hypertension", "pulmonary hypertension", "pediatric pulmonary hypertension", "pulmonary arterial hypertension", "macitentan", "selexipag", "ambrisentan", "bosentan", "sotatercept", "riociguat", "portopulmonary hypertension AND pulmonary hypertension", "echocardiography AND pulmonary hypertension", "CPET AND pulmonary hypertension", "PAH"]
    
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
            __database.save_to_database(__selected_dics)
            
            for __art_dic in __selected_dics:
                __art_dic['abstract'] = __translator.translate_abstract(__art_dic['abstract'])

            __results_dic[__query] = (__selected_dics, __n_found)
             
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
