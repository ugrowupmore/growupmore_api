# utils/pagination.py

from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

class KendoPagination(LimitOffsetPagination):
    default_limit = 10
    limit_query_param = 'take'
    offset_query_param = 'skip'

    def get_paginated_response(self, data):
        return Response({
            'take': self.get_limit(self.request),
            'skip': self.get_offset(self.request),
            'page': (self.get_offset(self.request) // self.get_limit(self.request)) + 1,
            'pageSize': self.get_limit(self.request),
            'total': self.count,
            'results': data
        })
