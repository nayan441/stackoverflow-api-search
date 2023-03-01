# middleware.py

from django.core.exceptions import PermissionDenied
from django.utils import timezone
from .models import SearchRecord

class SearchLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the current session ID
        session_id = request.session.session_key

        # Get the current timestamp
        now = timezone.now()

        # Count the number of searches made by this session in the past minute
        searches_last_minute = SearchRecord.objects.filter(
            session=session_id,
            timestamp__gte=now - timezone.timedelta(minutes=1)
        ).count()

        # Count the number of searches made by this session today
        searches_today = SearchRecord.objects.filter(
            session=session_id,
            timestamp__gte=timezone.now().date()
        ).count()

        # Check if the session has exceeded the limits
        if searches_last_minute >= 5 or searches_today >= 100:
            raise PermissionDenied("Search limit exceeded")

        # If the session has not exceeded the limits, update the search record
        SearchRecord.objects.create(session_id=session_id)

        response = self.get_response(request)

        return response
