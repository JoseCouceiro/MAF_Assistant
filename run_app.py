from display_info import Display
from search_pubmed import Search
from deepl_conect import Translate
from config import cfg_item
from user_params import get_params, add_search_to_database
import streamlit as st

__displayer = Display()
__searcher = Search()
__translator = Translate()
__class_params = cfg_item("classification_parameters")

def main(key):
    """
    Main function for the MAF Assistant application.

    This function displays a welcome message and prompts the user to enter their username. 
    If a username is provided, the placeholders for the title and username input are cleared. 
    The function then retrieves user-specific parameters and displays relevant information. 

    Parameters:
        key (str): A unique key used for Streamlit's text_input widget to maintain state.
    Returns:
        None
    """
    __title_placeholder = st.title('Welcome to MAF Assistant')
    __username_placeholder = st.empty()
    __user = __username_placeholder.text_input('Please, enter your username: ', key = key)
    if __user:
        __username_placeholder.empty()
        __title_placeholder.empty()
        __user_params = get_params(__user)
        if __user_params:
            __query_list = __user_params['search_terms']
        else:
            __query_list = []
        __displayer.display_title(__user)
        show_display(__user, __query_list)
        
def process_search(user, query_list, start_date, end_date, save_search):
    """
    Processes search queries for a user within a specified date range and optionally saves the search results.

    This function performs the following steps for each query in the query list:
    1. Runs the search.
    2. Removes duplicate results.
    3. Translates the abstracts of the selected articles.
    4. Displays information about the search and the selected articles.
    5. Optionally saves the search results to the database.

    Parameters:
        user (str): The identifier for the user performing the search.
        query_list (list): A list of search terms to be queried.
        start_date (str): The start date for the search range.
        end_date (str): The end date for the search range.
        save_search (bool): A flag indicating whether to save the search results to the database.
    Returns:
        None
    """
    __already_found = list()
    __results_dic = dict()
    if len(query_list) == 0:
        st.error('Please, add some search terms')
    for __query in query_list:
        __selected, __n_found = __searcher.run_search(__query, user, is_programmed=False, start_date=start_date, end_date=end_date)
        __selected_clean, __already_found = __searcher.remove_duplicates(__selected, __already_found)
        __selected_translated = __translator.translate_selected(__selected_clean)
        __displayer.display_search_info(__query, __n_found, __selected_translated)
        __displayer.display_article_info(__selected_translated)
        if save_search:
            __selected_dics = __searcher.transform_article_list(__selected_translated)
            __results_dic[__query] = (__selected_dics, __n_found)
            add_search_to_database(user, end_date, __results_dic)

def show_display(user, query_list):
    """
    Displays the user interface with multiple tabs for search functionalities.

    This function sets up and manages the display of four tabs in the Streamlit application:
    - Search: Allows the user to perform searches within a specified date range.
    - Search terms: Displays the user's search terms and provides options to add new terms or remove existing ones.
    - Classification parameters: Allows the user to set classification parameters.
    - Results archive: Displays the user's saved results.

    Parameters:
        user (str): The identifier for the user interacting with the interface.
        query_list (list): A list of search terms to be used in the search functionality.
    Returns:
        None
    """
    tab1, tab2, tab3, tab4 = st.tabs(['Search',
                                      'Search terms',
                                      'Classification parameters',
                                      'Results archive'])
    with tab1:
        __start_date_str, __end_date_str = __displayer.set_date()
        __search_on = __displayer.search_button()
        __save_search = __displayer.save_search_button()
        while __search_on:
            print('Running search')
            process_search(user, query_list, __start_date_str, __end_date_str, __save_search) 
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








