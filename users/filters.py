from rest_framework.filters import SearchFilter


class JWTBaseSearchFilter(SearchFilter):
    def get_search_terms(self, request):
        """
        Search terms are set by a ?search=... query parameter,
        and may be comma and/or whitespace delimited.
        """
        # request.query_params._mutable = True
        # request.query_params.update(request.jwt_data)
        params = str(request.jwt_data.get(self.search_param, ""))
        params = params.replace("\x00", "")  # strip null characters
        params = params.replace(",", " ")
        return params.split()
