from django.shortcuts import redirect
from django.urls import reverse
from user_app.models import Profile

class RoleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.user.is_authenticated:
            try:
                profile = request.user.profile
                request.role = profile.role
            except Profile.DoesNotExist:
                if 'profile-register/' not in request.path:
                    raise ValueError('complete the profile')
                else:
                    request.role = None



