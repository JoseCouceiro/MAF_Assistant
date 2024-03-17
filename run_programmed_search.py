from config import Config
from config import cfg_item
from config import SaveAndLoad
from search_pubmed import Search


__configurations = Config()
__configurations.instance()
__saveandload = SaveAndLoad()

#__query_list = cfg_item('search_terms')
__query_list = ["macitentan",
        "selexipag",
        "ambrisentan"]

__searcher = Search()

#__displayer.title

__programmed_search_on = __searcher.run_programmed_search()

while __programmed_search_on:
    print('Running search')
    __results_list = list()
    for __query in __query_list:
        __selected, __found = __searcher.run_search(__query, __programmed_search_on)
        print(f'{len(__selected)} selected out of {__found} found')
        __results_list.append(__selected)
        print(__selected)
    print(__results_list)
    __saveandload.save_history_file(__results_list)
        
    print('Search Done')
    __programmed_search_on = False
