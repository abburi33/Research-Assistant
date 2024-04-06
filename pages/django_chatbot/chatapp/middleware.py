from django.utils.cache import add_never_cache_headers

class NoCacheMiddleware:

    """
    Middleware to add cache control headers instructing clients not to cache responses.
    """
    def __init__(self, get_response):

        """
        Initializes the middleware.

        :param get_response: The get_response function.
        :type get_response: function
        """

        self.get_response = get_response




    def __call__(self, request):

        """
        Handles incoming requests and outgoing responses.

        :param request: The incoming HTTP request.
        :type request: django.http.HttpRequest
        :return: The HTTP response.
        :rtype: django.http.HttpResponse
        """

        response = self.get_response(request)
        add_never_cache_headers(response)
        return response
