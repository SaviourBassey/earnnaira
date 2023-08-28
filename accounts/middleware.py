from datetime import datetime, timedelta
from django.contrib.auth import logout
from django.utils import timezone

class DailyLogoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            current_time = timezone.now()
            last_login = request.user.last_login

            if last_login and last_login.date() < current_time.date():
                logout(request)
            elif last_login and last_login.date() == current_time.date():
                # Update the user's last login to avoid repeated logout on subsequent requests
                pass
                # request.user.last_login = current_time
                # request.user.save()

        response = self.get_response(request)
        return response
