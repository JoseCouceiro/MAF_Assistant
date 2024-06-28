import re
import os
import streamlit as st
from metapub import FindIt
from user_params import get_params, save_params, get_searches, save_searches

class Display():
    """
    This class contains all the necessary functions to display information in the streamlit application.
    """

    def display_title(self, user):
        """
        Function that displays the logo and name of the app.
        It also displays greetings to the user by using the function 'is_new_user' and a disclaimer to make sure it is the correct user.
        Input: username string.
        Output: streamlit display.
        """
        with st.sidebar:
            st.image(os.path.join('resources','images','logo.png'))
            self.is_new_user(user)        

    def is_new_user(self, user):
        """
        This function displays a disclaimer to inform the users whether they are new or not to the app.
        Input: username string.
        Output: streamlit display.
        """
        params = get_params(user)
        if params:
            st.markdown(f"Welcome back :orange['{user}']")
            st.markdown(f":orange[Not '{user}'?]: please, reload the page to enter your username")
        if not params:
            st.markdown(f"Your username is not in our database, welcome to MAF Assistant, '{user}'!")

    def search_button(self):
        """
        Function that displays a button that allows the user to start a search.
        Input: none.
        Output: streamlit display.
        """
        search_on = st.button("Start search", type="primary")
        return search_on
    
    def save_search_button(self):
        """
        Function that displays a checkbox that allows the user to save a search.
        Input: none.
        Output: streamlit display.
        """
        save_search = st.checkbox("Save search", key='Save search')
        return save_search
    
    def history_buttons(self, user):
        """
        This functions displays a button and checkbox for every search saved in the database. The searches are retrieved using the 'get_searches' function.
        When a button or checkbox is clicked, the corresponding search is saved to a list by its date (key).
        Searches in the 'deleting_buttons' list are removed from the list retrieved from the database and the updated list is saved back to the database.
        Searches saved in the list 'clicked_buttons' are returned by the function as a tuple containing both the entire search as a dictionary and the date as a string.
        Input: username string.
        Output: a tuple containing a dictionary and a string.
        """
        clicked_buttons = []
        deleting_buttons = []
        __saved_searches = get_searches(user)
        if __saved_searches:
            # Display buttons and checkboxes
            for __n, __key in enumerate(sorted(__saved_searches.keys())):
                button = st.button(f"{__key.replace('_', '/')}")
                checkbox = st.checkbox('Delete', key=f'checkbox_{__n}')
                # Save clicked buttons and checkboxes to lists
                if checkbox:
                    deleting_buttons.append(__key)
                    st.error("File '{}' deleted, uncheck the 'Delete' checkbox before continuing".format(__key.replace('_', '/')))
                if button and not checkbox:
                    clicked_buttons.append(__key)
            # Process delete actions after checking all buttons
            for __key in deleting_buttons:
                __saved_searches.pop(__key, None)
                save_searches(user, __saved_searches)
            # Return clicked filenames
            if len(clicked_buttons) != 0:
                return (__saved_searches[clicked_buttons[0]], clicked_buttons[0])

    def display_search_info(self, query, n_found, sel_list):
        """
        Function that takes in a query, the number of articles found and the list of selected articles and displays that information for the user.
        Input: string, integer, list.
        Output: streamlist display.
        """
        if sel_list != None:
            st.markdown(f":green[*Articles selected for query '{query}': {len(sel_list)} out of {n_found}*]")
        else:
            st.markdown(f":green[*No articles selected for query '{query}'*]")

    def __split_paragraphs(self, abst):
        """
        A function that takes a string as input and splits it into separate paragraphs at each occurrence of a word written entirely in uppercase.       
        Input: string.
        Output: string.
        """
        pattern = r'\b([A-ZÁÉÍÓÚÜÑ\s]+\:)'
        splitted = re.split(pattern, abst)
        return '\n'.join(splitted)
    
    def display_results(self, tup):
        """
        This function takes in a tuple containing an article object, a score and a boolean, then displays this information using Streamlit.     
        Input: a tuple containing an article object, an integer and a boolean.
        Output: a Streamlit display.
        """
        __art, __score, __pass = tup
        if __art != None:
            st.markdown(f"Article score: {__score}")
            st.markdown(f":red[**{__art.title}**]")
            st.markdown(__art.authors_str)
            st.markdown(f"https://doi.org/{__art.doi}")
            if __art.abstract != None:
                __splitted = self.__split_paragraphs(__art.abstract[0])
                if __art.abstract[1] == False:
                    st.error('DeepL translation quota exceeded')
                st.markdown(__splitted)
            try:
                __src = FindIt(str(__art.pmid))
                if __src.url:
                    st.markdown(__src.url)
                else:
                    st.markdown('No open access')
                    # st.markdown(__src.reason)
                st.markdown('\n')
            except:
                st.markdown('No open access')

    def display_history_results(self, tup):
        """
        This function takes in a tuple containing a query and an another tuple. This inner tuple contains a list of articles in dictionary format and an integer.
        The function displays this information using Streamlit.
        Input: a tuple containing a string an a tuple.
        Output: a Streamlit display.
        """
        for __query, __art_dup in tup[0].items():
            st.markdown(f":green[*Articles selected for query '{__query}' on {tup[1]}: {len(__art_dup[0])} out of {__art_dup[1]}*]")
            for __art in __art_dup[0]:
                st.markdown(f"Article score: {__art['score']}")
                st.markdown(f":red[**{__art['title']}**]")
                st.markdown(__art['authors_str'])
                st.markdown(f"https://doi.org/{__art['doi']}")
                if __art['abstract'] != None:
                    __splitted = self.__split_paragraphs(__art['abstract'])
                    if 'translated' in __art.keys(): #remove this line once the database is up to date
                        if __art['translated'] == False:
                            st.error('DeepL translation quota exceeded')
                    st.markdown(__splitted)
                try:
                    __src = FindIt(str(__art['pmid']))
                    if __src.url:
                        st.markdown(__src.url)
                    else:
                        st.markdown('No open access')
                        # st.markdown(__src.reason)
                    st.markdown('\n')
                except:
                    st.markdown('No open access')

    def show_search_terms(self, user):
        """
        Function that takes in a username as a string, searches the database for associated 'search terms' and displays the information using Streamlit.
        If no search terms are found, the function creates an empty list.
        The function then uses the functions 'append_search_term' and 'remove_search_term' to modify the database.
        Input: a string.
        Output: a Streamlit display.
        """
        st.markdown('**Search terms**')
        __user_params = get_params(user)
        if __user_params:
            if 'search_terms' in __user_params.keys():
                for __term in __user_params['search_terms']:
                    st.text(__term)
                    st.divider()
        else:
            __user_params = dict()
            __user_params['search_terms'] = []
            save_params(user, __user_params)
        
        self.__append_search_term(user, __user_params)
        self.__remove_search_term(user, __user_params)

    def __append_search_term(self, user, user_params):
        """
        This function accepts a username as a string and a dictionary of parameters. It then prompts for the input of new parameters.
        If a new parameter is provided, it is saved to the database.
        Input: a string and a dictionary.
        """
        __new_search_term = st.text_input('Add a new search term')
        if __new_search_term != "":
            user_params['search_terms'].append(__new_search_term)
            save_params(user, user_params)
            st.text('Term saved, please refresh page to update list')

    def __remove_search_term(self, user, user_params):
        """
        This function accepts a username as a string and a dictionary of parameters. It then prompts for the input of a parameter to be deleted.
        If the specified parameter provided exists in the database, it is removed.
        Input: a string and a dictionary.
        """
        __term_removed = st.text_input('Remove a search term')
        if __term_removed == "":
            pass
        elif __term_removed in user_params['search_terms']:          
            user_params['search_terms'].remove(__term_removed)
            save_params(user, user_params)
            st.text('Term removed, please refresh page to update list')
        else:
            st.error(f'{__term_removed} is not in the list of search terms')    

    def set_parameters(self, user, dic):
        """
        Function that prompts the user to set classification parameters and saves them to the database.
        This function displays input fields to set values for classification parameters using Streamlit. It retrieves existing parameters 
        for the user from the database. If parameters exist, it allows the user to update them. If not, it initializes 
        the parameters and allows the user to set them. All changes are saved to the database.
        Inputs:
            user : str
                The username for which the parameters are being set.
            dic : dict
                A dictionary mapping parameter keys to their descriptive names.
        Returns: none
        """
        st.markdown('**Classification parameters**')        
        __user_params = get_params(user)
        if __user_params:
            if 'selection_parameters' in __user_params.keys():
                for key, value in __user_params['selection_parameters'].items():
                    new_value = st.text_input(f"{dic[key]}:", value=value, key = key)
                    __user_params['selection_parameters'][key] = int(new_value)
                    save_params(user, __user_params)
            elif 'selection_parameters' not in __user_params.keys():
                __user_params['selection_parameters'] = dict()
                for key, val in dic.items():
                    new_value = st.text_input(f"{val}:", value=0)
                    __user_params['selection_parameters'][key] = int(new_value)
                    save_params(user, __user_params)



    