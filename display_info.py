import re
import json
import streamlit as st
from metapub import FindIt
from deepl_conect import Translate
from config import SaveAndLoad

class Display():

    def __init__(self):
        self.__transl = Translate()
        self.__saveandload = SaveAndLoad()
        self.tab1, self.tab2, self.tab3, self.tab4 = st.tabs(['Search results', 'Search terms', 'Classification parameters', 'Results archive'])
        self.__config_data = self.__saveandload.load_config_file()

    def search_button(self):
        search_on = st.button("Start search", type="primary")
        return search_on
        
    def __split_paragraphs(self, abst):
        pattern = r'\b([A-ZÁÉÍÓÚÜÑ\s]+\:)'
        splitted = re.split(pattern, abst)
        return '\n'.join(splitted)
    
    def display_results(self, tup):
        __art, __score = tup
        if __art != None:
            st.markdown(f'Article score: {__score}')
            st.markdown(f"**{__art.title}**")
            st.markdown(__art.authors_str)
            st.markdown(f'https://doi.org/{__art.doi}')
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

    def display_search_info(self, query, found, sel_list):
        if sel_list != None:
            st.markdown(f"*Articles selected for query '{query}': {len(sel_list)} out of {found}*")
        else:
            st.markdown(f"*No articles selected for query '{query}'*")

    def __append_search_term(self):
        __new_search_term = st.text_input('Add a new search term')
        if __new_search_term != "":
            self.__config_data['search_terms'].append(__new_search_term)
            self.__saveandload.save_config_file(self.__config_data)
            st.text('Term saved, please refresh page to update list')

    def __remove_search_term(self):
        __term_removed = st.text_input('Remove a search term')
        if __term_removed == "":
            pass
        elif __term_removed in self.__config_data['search_terms']:          
            self.__config_data['search_terms'].remove(__term_removed)
            self.__saveandload.save_config_file(self.__config_data)
            st.text('Term removed, please refresh page to update list')
        else:
            st.error(f'{__term_removed} is not in the list of search terms')    

    def show_search_terms(self):
            st.markdown('**Search terms**')
            for __term in self.__config_data['search_terms']:
                st.text(__term)
                st.divider()
            self.__append_search_term()
            self.__remove_search_term()
   
    def set_parameters(self):
            st.markdown('**Classification parameters**')
            dic = {'query_in_title': 'The query is in the title',
                   'is_rct': 'There is an rct in the journal',
                   'made_in_spain' : 'The journal was made in Spain',
                   'is_meta_analysis' : 'The journal is a meta_analysis?',
                   'from_countries' : 'The authors of the journal are from the countries of interest',
                   'threshold' : 'The journal should score above this value'}
            for key, value in self.__config_data['selection_parameters'].items():
                new_value = st.text_input(f"{dic[key]}:", value=value)
                self.__config_data['selection_parameters'][key] = int(new_value)
            self.__saveandload.save_config_file(self.__config_data)

    

    