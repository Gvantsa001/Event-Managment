from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size = 20  # Default page size
    page_size_query_param = 'page_size'  # Custom query parameter for setting page size
    max_page_size = 100  # Maximum page size allowed

    def get_paginated_response(self, data):
        response = super().get_paginated_response(data)
        response.data['custom_metadata'] = {
            'example_key': 'example_value'
        }
        return response