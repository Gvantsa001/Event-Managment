from django.urls import path
from . import views
from .views import EventListCreateAPIView, EventAPIView, CreateEventCreateAPIView,CreateEventRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('', views.getEvent),
    path('post/', views.postEvent),
    path('events/', EventListCreateAPIView.as_view(), name='event-list-create'),
    path('events/<int:pk>/', EventAPIView.as_view(), name='event-detail'),
    path('createvents/', CreateEventCreateAPIView.as_view(), name='create'),
    path('createvents/<int:pk>/', CreateEventRetrieveUpdateDestroyAPIView.as_view(), name='detail'),
]