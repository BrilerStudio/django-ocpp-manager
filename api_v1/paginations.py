from rest_framework.pagination import PageNumberPagination


class AdminPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    page_size = 20
    max_page_size = 100
