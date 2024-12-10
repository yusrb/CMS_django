from django.shortcuts import redirect
from django.urls import reverse
from admin_cms.models import User

class UserLevelMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        path = request.path

        return response

# user_cms/middleware.py
class ThemeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Logika middleware di sini
        response = self.get_response(request)
        return response

