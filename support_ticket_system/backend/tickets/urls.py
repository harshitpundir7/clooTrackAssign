from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import TicketViewSet, ticket_stats

router = DefaultRouter()
router.register(r'', TicketViewSet, basename='ticket')

urlpatterns = [
    # Stats endpoint must come before the router catch-all
    path('stats/', ticket_stats, name='ticket-stats'),
    path('', include(router.urls)),
]
