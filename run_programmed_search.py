from config import Config
from config import cfg_item
from search_pubmed import Search

__configurations = Config()
__configurations.instance()

#__query_list = cfg_item('search_terms')
__query_list = ["macitentan",
        "selexipag",
        "ambrisentan"]

__searcher = Search()

#__displayer.title

__programmed_search_on = __searcher.run_programmed_search()

while __programmed_search_on:
    print('Running search')
    for __query in __query_list:
        __selected, __found = __searcher.run_search(__query)
        print(f'{len(__selected)} selected out of {__found} found')
        print(__selected)
        
    print('Search Done')
    __programmed_search_on = False
