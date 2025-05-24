


"""
Write a custom Django middleware class that intercepts each incoming request.
Create a RequestlLog record in the database with the relevant request data.
Keep it efficient. 
"""

from django.utils.timezone import now
from django.db.utils import OperationalError, ProgrammingError
from .models import RequestLog

class LogRequestsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip logging for admin, static, media, and favicon
        path = request.path
        if path.startswith('/admin/') or path.startswith('/static/') or path.startswith('/favicon.ico'):
            return self.get_response(request)

        # Capture request details
        http_method = request.method
        full_path = request.get_full_path()

        # Make DB logging fail-safe and minimal
        try:
            RequestLog.objects.create(
                timestamp=now(),
                http_method=http_method,
                path=full_path,
            )
        except (OperationalError, ProgrammingError):
            # Database may not be ready (e.g., during migrations)
            pass

        return self.get_response(request)
