import logging
import time
from collections import defaultdict
from datetime import datetime, time

from django.http import HttpResponseForbidden, JsonResponse


class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only check role for authenticated users
        user = getattr(request, 'user', None)
        if user and user.is_authenticated:
            # Replace with actual check for role if you're using a custom user model or role field
            role = getattr(user, 'role', None)

            if role not in ['admin', 'moderator']:
                return JsonResponse(
                    {"error": "Access forbidden: Admins or moderators only."},
                    status=403
                )

        return self.get_response(request)


class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.requests = defaultdict(list)  # Stores request timestamps per IP
        self.limit = 5  # messages
        self.window = 60  # seconds

    def __call__(self, request):
        # Apply rate limiting only to POST requests to messages endpoint
        if request.method == "POST" and request.path.startswith("/api/messages/"):
            ip = self.get_client_ip(request)
            now = time.time()

            # Keep only timestamps within the last 60 seconds
            self.requests[ip] = [t for t in self.requests[ip] if now - t < self.window]

            if len(self.requests[ip]) >= self.limit:
                return JsonResponse(
                    {"error": "Rate limit exceeded: Only 5 messages allowed per minute."},
                    status=429
                )

            # Store this request's timestamp
            self.requests[ip].append(now)

        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get("REMOTE_ADDR", "")

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_time = datetime.now().time()

        # Define allowed access window: between 6PM and 9PM
        start_time = time(18, 0)  # 6:00 PM
        end_time = time(21, 0)  # 9:00 PM

        # Restrict access if outside the window
        if not (start_time <= current_time <= end_time):
            if request.path.startswith("/api/messages/") or request.path.startswith("/api/conversations/"):
                return HttpResponseForbidden("Access to chat is only allowed between 6PM and 9PM.")

        return self.get_response(request)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Configure logger
        self.logger = logging.getLogger("request_logger")
        handler = logging.FileHandler("requests.log")
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(handler)

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        self.logger.info(f"{datetime.now()} - User: {user} - Path: {request.path}")

        response = self.get_response(request)
        return response
