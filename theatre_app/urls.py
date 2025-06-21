from django.urls import path
from . import views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Theatre API",
      default_version='v1',
      description="API for online ticket booking",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('actors/', views.ActorListView.as_view(), name='actor-list'),
    path('genres/', views.GenreListView.as_view(), name='genre-list'),

    path('plays/', views.PlayListView.as_view(), name='play-list'),
    path('plays/<int:pk>/', views.PlayDetailView.as_view(), name='play-detail'),

    path('theatre-halls/', views.TheatreHallListView.as_view(), name='theatrehall-list'),

    path('performances/', views.PerformanceListView.as_view(), name='performance-list'),
    path('performances/<int:pk>/', views.PerformanceDetailView.as_view(), name='performance-detail'),

    path('reservations/', views.ReservationListCreateView.as_view(), name='reservation-list-create'),

    path('tickets/', views.TicketListCreateView.as_view(), name='ticket-list-create'),
    path('performances/<int:performance_id>/available-seats/', views.available_seats, name='available-seats'),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
