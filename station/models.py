import os
import uuid

from django.db import models
from django.db.models import UniqueConstraint
from django.utils.text import slugify
from rest_framework.exceptions import ValidationError

from train_station import settings


class Crew(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Station(models.Model):
    name = models.CharField(max_length=60, unique=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=2)
    longitude = models.DecimalField(max_digits=9, decimal_places=2)

    def __str__(self):
        return self.name


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return str(self.created_at)

    class Meta:
        ordering = ["-created_at"]


class TrainType(models.Model):
    name = models.CharField(max_length=60, unique=True)

    def __str__(self):
        return self.name


def train_image_path(instance, filename):
    _, extension = os.path.splitext(filename)
    return os.path.join(
        f"uploads/train/",
        f"{slugify(instance.name)}-{uuid.uuid4()}.{extension}"
    )


class Train(models.Model):
    name = models.CharField(max_length=60)
    cargo_num = models.IntegerField()
    places_in_cargo = models.IntegerField()
    train_type = models.ForeignKey(TrainType, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=train_image_path, blank=True)

    def __str__(self):
        return self.name


class Route(models.Model):
    source = models.ForeignKey(
        Station,
        on_delete=models.CASCADE,
        related_name="source_routes"
    )
    destination = models.ForeignKey(
        Station,
        on_delete=models.CASCADE,
        related_name="destination_routes"
    )
    distance = models.IntegerField()

    class Meta:
        indexes = [
            models.Index(fields=["source", "destination"])
        ]

    @staticmethod
    def validate_route(source: str, destination: str):
        if not (source != destination):
            raise ValidationError(
                {
                    "source": "The source and destination cannot be the same"
                }
            )

    def clean(self):
        Route.validate_route(
            self.source.name,
            self.destination.name
        )

    @property
    def route(self):
        return f"{self.source} -> {self.destination}"

    def __str__(self):
        return f"{self.source} -> {self.destination}: {self.distance}"


class Journey(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    crew = models.ManyToManyField(Crew, related_name="journeys")

    class Meta:
        indexes = [
            models.Index(fields=["departure_time", "arrival_time"])
        ]

    def __str__(self):
        return (f"Journey from {self.route.source.name} "
                f"to {self.route.destination.name} "
                f"by {self.train.name}")


class Ticket(models.Model):
    cargo = models.IntegerField()
    seat = models.IntegerField()
    journey = models.ForeignKey(
        Journey,
        on_delete=models.CASCADE,
        related_name="tickets"
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="tickets"
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["cargo", "seat", "journey"],
                name="unique_ticket"
            )
        ]
        ordering = ["cargo", "seat"]

    @staticmethod
    def validate_ticket(seat: int,
                        places_in_cargo: int,
                        cargo: int,
                        cargo_num: int):
        if not (1 <= seat <= places_in_cargo):
            raise ValidationError(
                {
                    "seat": f"Seat must be in range "
                            f"[1, {places_in_cargo}], not {seat}"
                }
            )
        if not (1 <= cargo <= cargo_num):
            raise ValidationError(
                {
                    "cargo": f"Cargo must be in range "
                             f"[1, {cargo_num}], not {cargo}"
                }
            )

    def clean(self):
        Ticket.validate_ticket(self.seat,
                               self.journey.train.places_in_cargo,
                               self.cargo,
                               self.journey.train.places_in_cargo)

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None
    ):
        self.full_clean()
        return super(Ticket, self).save(
            force_insert,
            force_update,
            using,
            update_fields
        )

    def __str__(self):
        return f"cargo: {self.cargo}, seat: {self.seat}"
