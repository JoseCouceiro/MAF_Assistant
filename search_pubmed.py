from metapub import PubMedFetcher
import streamlit as st
from classify_articles import Classify
from config import SaveAndLoad

class Search:
    """
    A class that provides functions for connecting to PubMed via Metapub, performing searches, and curating the search results.
    """

    def __init__(self):
        self.__fetcher = PubMedFetcher()
        self.__classifier = Classify()
        self.__saveandload = SaveAndLoad()
        self.__config_data = self.__saveandload.load_config_file()
        
    def __search_pubmed(self, query, start_date, end_date):
        """
        Function that searches PubMed for articles matching the given query within the specified date range.
        This function constructs a PubMed search query using the provided search terms and date range,
        fetches the PubMed IDs (PMIDs) of the matching articles, and returns them.
        Inputs:
            query : str
                The search terms to use for querying PubMed. This will be searched within the title and abstract of articles.
            start_date : str
                The start date for the publication date range, in the format 'YYYY-MM-DD'.
            end_date : str
                The end date for the publication date range, in the format 'YYYY-MM-DD'.
        Output:
            list
                A list of PubMed IDs (PMIDs) for articles that match the search query within the specified date range.

        """
        pmids = self.__fetcher.pmids_for_query(
            f'({query}[Title/Abstract]) AND ("{start_date}"[Date - Publication] : "{end_date}"[Date - Publication])')
        print(f'({query}[Title/Abstract]) AND ("{start_date}"[Date - Publication] : "{end_date}"[Date - Publication])')
        return pmids

    def __fetch_articles(self, pmids_list, query, user, is_programmed):
        """
        This function fetches and classifies articles from PubMed based on a list of PMIDs, then sorts and returns them.
        Articles are retrieved from PubMed using a list of PMIDs, classified according to
        the specified query and user criteria, and separated into selected and rejected categories.
        The selected articles can be returned either sorted by their score or as-is, depending on the 'is_programmed' flag.
        Inputs:
            pmids_list: list
                A list of PubMed IDs (PMIDs) to fetch articles for.
            query: str
                The search query used for classification.
            user: str
                The username to be passed to the 'rater' function.
            is_programmed : bool
                A flag indicating whether to return the selected articles sorted by their score (False) or as-is (True).
        Output:
            tuple
            A tuple containing two lists:
            - A list of selected articles, each represented as a tuple of the article object, its score, and a boolean pass/fail.
            - A list of rejected articles, each represented as a tuple of the article object, its score, and a boolean pass/fail.
        """
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
        """
        Transforms a list of article tuples into a list of dictionaries.
        This function takes a list of tuples representing articles and transforms each tuple into a dictionary.
        Each dictionary contains selected fields extracted from the article.
        Inputs:
            art_list: list
                A list of tuples, where each tuple contains an article object, its score, and a boolean indicating selection.
        Output: list
                A list of dictionaries, where each dictionary represents an article.
        """
        transformed_art_list = list()
        for __tup in art_list:
            __art_dic = dict()
            __art, __score, __pass = __tup
            __art_dic['title'] = __art.title
            __art_dic['authors_str'] = __art.authors_str
            __art_dic['doi'] = __art.doi
            if __art.abstract:
                __art_dic['abstract'] = __art.abstract[0]
                __art_dic['translated'] = __art.abstract[1]
            else:
                __art_dic['abstract'] = None
                __art_dic['translated'] = None
            __art_dic['pmid'] = __art.pmid
            __art_dic['score'] = __score
            __art_dic['selected'] = __pass
            transformed_art_list.append(__art_dic)
        return transformed_art_list

    def run_search(self, query, user, is_programmed, start_date, end_date):
        """
        Executes a PubMed search and processes the retrieved articles based on provided parameters.
        This function initiates a PubMed search using the specified query and date range. It retrieves PubMed IDs (PMIDs) 
        for articles matching the search criteria, fetches and classifies these articles, and optionally returns the 
        selected articles, rejected articles, and the total number of articles found.
        Inputs:
            query: str
                The search query to be executed on PubMed.
            user: str
                The username to be passed to the 'fetch_articles' function.
            is_programmed: bool
                A flag indicating whether to return sorted selected articles only (False) or both selected and rejected articles (True).
            start_date: str
                The start date for the publication date range of the articles to be searched, in 'YYYY-MM-DD' format.
            end_date: str
                The end date for the publication date range of the articles to be searched, in 'YYYY-MM-DD' format.
        Returns: tuple
                If 'is_programmed' is False, returns a tuple containing:
                    - A list of selected articles, each represented as a tuple of article object, score, and boolean pass/fail.
                    - The total number of articles found matching the query.
                If 'is_programmed' is True, returns a tuple containing:
                    - A list of selected articles, each represented as a tuple of article object, score, and boolean pass/fail.
                    - A list of rejected articles, each represented as a tuple of article object, score, and boolean pass/fail.
                    - The total number of articles found matching the query.
        """
        __pmids = self.__search_pubmed(query, start_date, end_date)
        __n_found = len(__pmids)
        print('Number of articles found: ', len(__pmids))
        __selected, __rejected = self.__fetch_articles(__pmids, query, user, is_programmed)
        if not is_programmed:
            return __selected, __n_found
        if is_programmed:
            return __selected, __rejected, __n_found
        
    def remove_duplicates(self, selected_list, duplicates_list):
        """
        Removes duplicates from a list of selected articles based on their PubMed IDs (PMIDs).
        This function iterates through a list of selected articles represented as tuples, each containing an article object,
        its score, and a boolean indicating selection. It checks if the article's PMID already exists in the duplicates_list.
        If a duplicate is found, it removes the article from the selected_list. If not, it adds the article's PMID to the duplicates_list.
        Inputs:
            selected_list: list
                A list of tuples representing selected articles, where each tuple contains an article object, its score, and a boolean pass/fail.
            duplicates_list: list
                A list containing PMIDs (PubMed IDs) of articles that have already been selected.
        Output: tuple
            A tuple containing:
            - The updated list of selected articles after removing duplicates.
            - The updated duplicates_list containing PMIDs of all processed articles.

        """
        if len(selected_list) != 0:
            for __tup in selected_list:
                __art, __score, __pass = __tup
                if __art.pmid in duplicates_list:
                    selected_list.remove(__tup)
                else:
                    duplicates_list.append(__art.pmid)
        return selected_list, duplicates_list

    
    
            



    

