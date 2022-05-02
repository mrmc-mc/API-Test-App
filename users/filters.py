# from rest_framework import filters

# class JWTBaseSearchFilter(filters.SearchFilter):
#     def get_search_fields(self, view, request):
#         if request.jwt_data('email'):
#             return ['email']
#         return super().get_search_fields(view, request)