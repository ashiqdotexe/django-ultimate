from rest_framework.pagination import PageNumberPagination

class PaginationNumber(PageNumberPagination):
    page_size = 10