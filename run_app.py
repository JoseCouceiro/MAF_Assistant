from display_info import Display
from search_pubmed import Search
from config import Config
from config import cfg_item

__configurations = Config()
__configurations.instance()

#__query_list = cfg_item('search_terms')
__query_list = ["macitentan",
        "selexipag"]

__displayer = Display()
__searcher = Search()

with __displayer.tab3:
    __displayer.set_parameters()

with __displayer.tab2:    
    __displayer.show_search_terms()

with __displayer.tab4:
    'saved searches'

with __displayer.tab1:
    if __searcher.dayly_search_done == False:
        if __searcher.is_searching_day():
            __search_on = True
            __searcher.dayly_search_done = True
        else:
            __search_on = __displayer.search_button()

    


    while __search_on:
        print('Running search')
        for __query in __query_list:
            __selected, __found = __searcher.run_search(__query)
            __displayer.display_search_info(__query, __found, __selected)
            for __tup in __selected:
                __displayer.display_results(__tup)
        print('Search Done')
        __search_on = False






