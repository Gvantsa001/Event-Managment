from events.models import Event
from events.serializers import EventSerializer
from rest_framework import permissions
class IsEventManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_event_manager

from rest_framework import viewsets


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsEventManager]  # Apply the custom permission class

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

class CanAddEventsPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_event_manager