from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.serializers import ModelSerializer
from .models import Actor, Genre, Play, TheatreHall, Performance, Reservation, Ticket
from .serializers import (
    ActorSerializer,
    GenreSerializer,
    PlaySerializer,
    TheatreHallSerializer,
    PerformanceSerializer,
    ReservationSerializer,
    TicketSerializer,
)


@api_view(['GET'])
def available_seats(request, performance_id):
    performance = Performance.objects.get(id=performance_id)
    hall = performance.theatre_hall
    all_seats = {(row, seat) for row in range(1, hall.rows + 1) for seat in range(1, hall.seats_in_row + 1)}
    booked_seats = set(Ticket.objects.filter(performance=performance).values_list('row', 'seat'))
    available = all_seats - booked_seats
    return Response(sorted(available))


class ActorListView(generics.ListAPIView):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer


class GenreListView(generics.ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class PlayListView(generics.ListAPIView):
    queryset = Play.objects.all()
    serializer_class = PlaySerializer


class PlayDetailView(generics.RetrieveAPIView):
    queryset = Play.objects.all()
    serializer_class = PlaySerializer


class TheatreHallListView(generics.ListAPIView):
    queryset = TheatreHall.objects.all()
    serializer_class = TheatreHallSerializer


class PerformanceListView(generics.ListAPIView):
    queryset = Performance.objects.all()
    serializer_class = PerformanceSerializer


class PerformanceDetailView(generics.RetrieveAPIView):
    queryset = Performance.objects.all()
    serializer_class = PerformanceSerializer


class ReservationListCreateView(generics.ListCreateAPIView):
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TicketListCreateView(generics.ListCreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        performance = serializer.validated_data['performance']
        row = serializer.validated_data['row']
        seat = serializer.validated_data['seat']

        if Ticket.objects.filter(performance=performance, row=row, seat=seat).exists():
            raise serializers.ValidationError("This place is already taken.")
    
        serializer.save()


class RegisterSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer