from django.db.models import Count, Q, Min
from django.utils import timezone
from rest_framework import viewsets, status, filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Ticket
from .serializers import TicketSerializer


class TicketViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Ticket CRUD operations.

    POST   /api/tickets/          — Create a new ticket (returns 201)
    GET    /api/tickets/          — List all tickets, newest first
    PATCH  /api/tickets/<id>/     — Update a ticket
    GET    /api/tickets/<id>/     — Retrieve a single ticket
    """

    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'priority', 'status']
    search_fields = ['title', 'description']
    ordering = ['-created_at']


@api_view(['GET'])
def ticket_stats(request):
    """
    GET /api/tickets/stats/

    Returns aggregated ticket statistics using DB-level aggregation
    (Django ORM aggregate/annotate — no Python-level loops).
    """
    total_tickets = Ticket.objects.count()
    open_tickets = Ticket.objects.filter(status='open').count()

    # Average tickets per day: total / number_of_days since the first ticket
    first_ticket = Ticket.objects.aggregate(first=Min('created_at'))['first']
    if first_ticket:
        days_since_first = (timezone.now() - first_ticket).days or 1
        avg_tickets_per_day = round(total_tickets / days_since_first, 1)
    else:
        avg_tickets_per_day = 0

    # Priority breakdown via DB-level aggregation
    priority_qs = (
        Ticket.objects
        .values('priority')
        .annotate(count=Count('id'))
    )
    priority_breakdown = {
        choice: 0 for choice, _ in Ticket.PRIORITY_CHOICES
    }
    for item in priority_qs:
        priority_breakdown[item['priority']] = item['count']

    # Category breakdown via DB-level aggregation
    category_qs = (
        Ticket.objects
        .values('category')
        .annotate(count=Count('id'))
    )
    category_breakdown = {
        choice: 0 for choice, _ in Ticket.CATEGORY_CHOICES
    }
    for item in category_qs:
        category_breakdown[item['category']] = item['count']

    return Response({
        'total_tickets': total_tickets,
        'open_tickets': open_tickets,
        'avg_tickets_per_day': avg_tickets_per_day,
        'priority_breakdown': priority_breakdown,
        'category_breakdown': category_breakdown,
    })
