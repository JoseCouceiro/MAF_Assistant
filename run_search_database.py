from config import Config
from config import SaveAndLoad
from config import DataBase
from deepl_conect import Translate
from user_params import save_searches, get_searches, get_params
from search_pubmed import Search

__configurations = Config()
__configurations.instance()
__database = DataBase()
__searcher = Search()

__user = input('Introduce your username: ')
__start_date = input('Start date ("YYYY/MM/DD" format): ')
__end_date = input('End date ("YYYY/MM/DD" format): ')
__query_list = get_params(__user)['search_terms']

if __user:
    print('Running search')
    __already_found = list()
    for __query in __query_list:
        __selected, __rejected, __n_found = __searcher.run_search(__query, __user, is_programmed=True, start_date=__start_date, end_date=__end_date)
        __selected_clean, __already_found = __searcher.remove_duplicates(__selected, __already_found)
        print(f'{len(__selected)} selected out of {__n_found} found')
        
        __selected_dics = __searcher.transform_article_list(__selected_clean)
        __rejected_dics = __searcher.transform_article_list(__rejected) 
        __database.save_to_database(__selected_dics)
        __database.save_to_database(__rejected_dics)
        print('Database updated')
    print('Search Done')

