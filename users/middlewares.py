from django.contrib.auth import get_user_model


User = get_user_model()

class ActiveEmailMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        
        if not request.user.is_email_verified:
                pass

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response