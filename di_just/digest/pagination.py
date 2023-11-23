from rest_framework import pagination
from rest_framework.response import Response
from collections import OrderedDict


# в данном файле прописана кастомная пагинация
class CustomPagination(pagination.PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'  # количество записей на одной странице
    max_page_size = 50
    page_query_param = 'p'  # номер страницы

    # данная функция возвращает запрос, добавляя в хедер информацию о пагинации (следующая и предыдущая страницы)
    def get_paginated_response(self, data):
        response = Response(data)
        response['count'] = self.page.paginator.count
        response['next'] = self.get_next_link()
        response['previous'] = self.get_previous_link()
        return response
