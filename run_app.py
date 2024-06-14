from display_info import Display
from search_pubmed import Search
from deepl_conect import Translate
from config import DataBase
from config import cfg_item
from user_params import get_params, save_params, get_searches, save_searches
import streamlit as st

__displayer = Display()
__searcher = Search()
__database = DataBase()
__translator = Translate()
__class_params = cfg_item("classification_parameters")

def main(key):
    __title_placeholder = st.title('Welcome to MAF Assistant')
    __username_placeholder = st.empty()
    __user = __username_placeholder.text_input('Please, enter your username: ', key = key)
    if __user:
        __user_params = get_params(__user)
        if __user_params:
            __query_list = __user_params['search_terms']
        else:
            __query_list = []
        __displayer.display_title(__user)
        show_display(__user, __query_list)
        __username_placeholder.empty()
        __title_placeholder.empty()   

def show_display(user, query_list):
    tab1, tab2, tab3, tab4 = st.tabs(['Search results',
                                      'Search terms',
                                      'Classification parameters',
                                      'Results archive'])
    with tab1:
        __search_on = __displayer.search_button()
        __save_search = __displayer.save_search_button()
        __date = '14/06/2024'
        while __search_on:
            print('Running search')
            __already_found = list()
            __results_dic = dict()
            if len(query_list) == 0:
                st.error('Please, add some search terms')
            for __query in query_list:
                __selected, __rejected, __n_found = __searcher.run_search(__query, user, is_programmed=True)
                __selected_clean, __already_found = __searcher.remove_duplicates(__selected, __already_found)
                __displayer.display_search_info(__query, __n_found, __selected_clean)
                try:
                    for __tup in __selected_clean:
                        __displayer.display_results(__tup)
                except:
                    st.write('Journal has already been selected in a different query')
                    
                if __save_search:
                    __selected_dics = __searcher.transform_article_list(__selected_clean)
                    __rejected_dics = __searcher.transform_article_list(__rejected) 
                    __database.save_to_database(__selected_dics)
                    __database.save_to_database(__rejected_dics)
                    print('Database updated')
            
                    for __art_dic in __selected_dics:
                        __art_dic['abstract'] = __translator.translate_abstract(__art_dic['abstract'])

                    __results_dic[__query] = (__selected_dics, __n_found)

            __save_searches_dic = get_searches(user)
            if __save_searches_dic:
                __save_searches_dic[__date] = __results_dic
            else:
                __save_searches_dic = dict()
                __save_searches_dic[__date] = __results_dic
            save_searches(user, __save_searches_dic)
            
            print('Search Done')
            __search_on = False
        

    with tab2:    
        __displayer.show_search_terms(user)

    with tab3:
        __displayer.set_parameters(user, __class_params)

    with tab4:
        col1, col2 = st.columns([1,4])

        with col1:
            __saved_search = __displayer.history_buttons(user)
        with col2:
            if __saved_search:             
                __displayer.display_history_results(__saved_search)

if __name__ == '__main__':
    main('first')








