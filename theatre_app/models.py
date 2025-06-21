from django.db import models
from django.contrib.auth.models import User


class Actor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Play(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    actors = models.ManyToManyField(Actor, related_name='plays', blank=True)
    genres = models.ManyToManyField(Genre, related_name='plays', blank=True)

    def __str__(self):
        return self.title


class TheatreHall(models.Model):
    name = models.CharField(max_length=100)
    rows = models.PositiveIntegerField()
    seats_in_row = models.PositiveIntegerField()

    def __str__(self):
        return self.name

    def capacity(self):
        return self.rows * self.seats_in_row


class Performance(models.Model):
    play = models.ForeignKey(Play, on_delete=models.CASCADE, related_name='performances')
    theatre_hall = models.ForeignKey(TheatreHall, on_delete=models.CASCADE, related_name='performances')
    show_time = models.DateTimeField()

    def __str__(self):
        return f"{self.play.title} @ {self.show_time}"


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reservation #{self.id} by {self.user.username}"


class Ticket(models.Model):
    row = models.PositiveIntegerField()
    seat = models.PositiveIntegerField()
    performance = models.ForeignKey(Performance, on_delete=models.CASCADE, related_name='tickets')
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='tickets')

    class Meta:
        unique_together = ('row', 'seat', 'performance')

    def __str__(self):
        return f"Seat {self.row}-{self.seat} for {self.performance}"
