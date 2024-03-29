from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Event, CreateEvent
from .serializers import EventSerializer, CreateEventSerializer
from rest_framework import viewsets
from rest_framework import generics
from .pagination import CustomPagination


@api_view(['GET'])
def getEvent(request):
   events = Event.objects.all()
   serializer = EventSerializer(events, many=True)
   return Response()



@api_view(['POST'])
def postEvent(request):
   return Response()



class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class EventListCreateAPIView(generics.ListCreateAPIView):
   queryset = Event.objects.all()
   serializer_class = EventSerializer


class EventAPIView(generics.RetrieveUpdateDestroyAPIView):
   queryset = Event.objects.all()
   serializer_class = EventSerializer

class CreateEventCreateAPIView(generics.CreateAPIView):
    queryset = CreateEvent.objects.all()
    serializer_class = CreateEventSerializer

class CreateEventRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CreateEvent.objects.all()
    serializer_class = CreateEventSerializer

class YourModelListView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    pagination_class = CustomPagination
