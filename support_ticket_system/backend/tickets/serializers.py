from rest_framework import serializers
from .models import Ticket


class TicketSerializer(serializers.ModelSerializer):
    """Serializer for the Ticket model."""

    class Meta:
        model = Ticket
        fields = [
            'id', 'title', 'description', 'category',
            'priority', 'status', 'created_at',
        ]
        read_only_fields = ['id', 'created_at']
