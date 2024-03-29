from rest_framework import serializers
from .models import Event, CreateEvent


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'start_date', 'end_date', 'location', 'organizer','tickets_number']

    def create(self, validated_data):
        user = self.context['request'].user
        if not user.can_add_events:
            raise serializers.ValidationError("You do not have permission to add events.")

        return super().create(validated_data)

class CreateEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreateEvent
        fields = ['id', 'title', 'content', 'location', 'organizer', 'created_at']