import logging
from datetime import datetime
import time
from django.http import HttpResponseForbidden, JsonResponse


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        logging.basicConfig(filename='requests.log', level=logging.INFO)

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        log_msg = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logging.info(log_msg)
        return self.get_response(request)


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour
        if request.path.startswith("/api/") and (current_hour < 6 or current_hour > 21):
            return HttpResponseForbidden("Chat access is only allowed between 6 AM and 9 PM.")
        return self.get_response(request)


class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.message_logs = {}  # IP: [timestamp1, timestamp2, ...]

    def __call__(self, request):
        if request.method == 'POST' and request.path.startswith('/api/messages'):
            ip = request.META.get('REMOTE_ADDR', 'unknown')
            now = time.time()
            self.message_logs.setdefault(ip, [])
            # Keep only timestamps within the last 60 seconds
            self.message_logs[ip] = [t for t in self.message_logs[ip] if now - t < 60]
            if len(self.message_logs[ip]) >= 5:
                return JsonResponse({'error': 'Message limit exceeded (5 per minute)'}, status=429)
            self.message_logs[ip].append(now)
        return self.get_response(request)


class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/api/messages'):
            user = request.user
            if not user.is_authenticated or not user.groups.filter(name__in=['admin', 'moderator']).exists():
                return HttpResponseForbidden("Only admins and moderators can access this endpoint.")
        return self.get_response(request)
