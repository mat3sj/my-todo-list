from django.http import HttpResponseRedirect
from django.urls import reverse


class AuthRequiredMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == ('/login/'):
            return self.get_response(request)
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/login/')  # or http response
        return self.get_response(request)

