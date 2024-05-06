import re
import os
from pathlib import Path
import streamlit as st
from metapub import FindIt
from deepl_conect import Translate
from config import SaveAndLoad
from user_params import get_params, save_params

class Display():

    def __init__(self):
        self.__transl = Translate()
        self.__saveandload = SaveAndLoad()
        #self.tab1, self.tab2, self.tab3, self.tab4 = st.tabs(['Search results', 'Search terms', 'Classification parameters', 'Results archive'])
        #with self.tab4:
            #self.col1, self.col2 = st.columns([1,4])
        self.__config_data = self.__saveandload.load_config_file()
        self.__searches_path = Path(os.path.join("resources", "saved_searches"))

    def display_title(self, user):
        with st.sidebar:
            st.markdown('**MAF ASSISTANT**')
            st.markdown('A tool for automated pubmed searching')
            self.is_new_user(user)        

    def is_new_user(self, user):
        params = get_params(user)
        if params:
            st.write(f'Welcome back {user} \n\n Not {user}?: please, reload to enter your username')
        if not params:
            st.write(f'Your username is not in our database, welcome to MAF Assistant, {user}!')

    def search_button(self):
        search_on = st.button("Start search", type="primary")
        return search_on
    
    def history_buttons(self):
        filenames = dict()
        clicked_buttons = []
        deleting_buttons = []
        for __n, __file in enumerate(self.__searches_path.iterdir()): 
            filenames[__n] = __file.name.split('.')[0]
            button = st.button(f"{filenames[__n].replace('_', '/')}")
            checkbox = st.checkbox('Delete', key=f'checkbox_{__n}')
            if checkbox:
                deleting_buttons.append(__n)
                #st.error(f"File '{__file.name.split(".")[0]}' deleted, uncheck the 'Delete' checkbox before continuing")
                st.error('File "{}" deleted, uncheck the "Delete" checkbox before continuing'.format(__file.name.split('.')[0]))
            if button and not checkbox:
                clicked_buttons.append(__n)
        # Process delete actions after checking all buttons
        for __n in deleting_buttons:
            filename = filenames[__n] + '.json'
            os.remove(os.path.join(self.__searches_path, filename))
        # Return clicked filenames
        if len(clicked_buttons) != 0:
            return filenames[clicked_buttons[0]]
       
    def __split_paragraphs(self, abst):
        pattern = r'\b([A-ZÁÉÍÓÚÜÑ\s]+\:)'
        splitted = re.split(pattern, abst)
        return '\n'.join(splitted)
    
    def display_results(self, tup):
        __art, __score, __pass = tup
        if __art != None:
            st.markdown(f"Article score: {__score}")
            st.markdown(f"**{__art.title}**")
            st.markdown(__art.authors_str)
            st.markdown(f"https://doi.org/{__art.doi}")
            if __art.abstract != None:
                __splitted = self.__split_paragraphs(__art.abstract)
                try:
                    st.markdown(self.__transl.translate_to_sp(__splitted))
                except:
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

    def display_history_results(self, dic):
        for __query, __art_lst in dic.items():
            st.markdown(f"*Articles selected for query '{__query}': {len(__art_lst)}*")
            for __art in __art_lst:
                st.markdown(f"Article score: {__art['score']}")
                st.markdown(f"**{__art['title']}**")
                st.markdown(__art['authors_str'])
                st.markdown(f"https://doi.org/{__art['doi']}")
                if __art['abstract'] != None:
                    __splitted = self.__split_paragraphs(__art['abstract'])
                    try:
                        st.markdown(self.__transl.translate_to_sp(__splitted))
                    except:
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

    def display_search_info(self, query, n_found, sel_list):
        if sel_list != None:
            st.markdown(f"*Articles selected for query '{query}': {len(sel_list)} out of {n_found}*")
        else:
            st.markdown(f"*No articles selected for query '{query}'*")

    def __append_search_term(self, user, user_params):
        __new_search_term = st.text_input('Add a new search term')
        if __new_search_term != "":
            user_params['search_terms'].append(__new_search_term)
            save_params(user, user_params)
            st.text('Term saved, please refresh page to update list')

    def __remove_search_term(self, user, user_params):
        __term_removed = st.text_input('Remove a search term')
        if __term_removed == "":
            pass
        elif __term_removed in user_params['search_terms']:          
            user_params['search_terms'].remove(__term_removed)
            save_params(user, user_params)
            st.text('Term removed, please refresh page to update list')
        else:
            st.error(f'{__term_removed} is not in the list of search terms')    

    def show_search_terms(self, user):
        st.markdown('**Search terms**')
        __user_params = get_params(user)
        st.write(__user_params)
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

    def set_parameters(self, user):
        
        st.markdown('**Classification parameters**')
        dic = {'query_in_title': 'The query is in the title',
                'is_rct': 'There is an rct in the journal',
                'made_in_spain' : 'The journal was made in Spain',
                'is_meta_analysis' : 'The journal is a meta_analysis',
                'from_countries' : 'The authors of the journal are from the countries of interest',
                'threshold' : 'The journal should score above this value'}
        
        __user_params = get_params(user)

        if __user_params:
            if 'selection_parameters' in __user_params.keys():
                for key, value in __user_params['selection_parameters'].items():
                    new_value = st.text_input(f"{dic[key]}:", value=value, key = key)
                    st.write(new_value)
                    __user_params['selection_parameters'][key] = int(new_value)
                    save_params(user, __user_params)
            elif 'selection_parameters' not in __user_params.keys():
                __user_params['selection_parameters'] = dict()
                for key, val in dic.items():
                    new_value = st.text_input(f"{val}:", value=0)
                    st.write(new_value)
                    __user_params['selection_parameters'][key] = int(new_value)
                    st.write(__user_params)
                    save_params(user, __user_params)



    