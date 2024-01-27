from rest_framework.filters import SearchFilter


class ReactSearchFilter(SearchFilter):
    search_param = 'q'
