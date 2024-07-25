from django.db import transaction
from rest_framework import serializers

from station.models import Station, Crew, Journey, Route, Train, TrainType, Order, Ticket


class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = ("id", "name", "latitude", "longitude",)


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = ("id", "first_name", "last_name", "full_name")


class TrainTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainType
        fields = ("id", "name",)


class TrainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Train
        fields = ("id", "name", "cargo_num", "places_in_cargo", "train_type",)


class TrainListSerializer(serializers.ModelSerializer):
    train_type = serializers.CharField(source="train_type.name", read_only=True)

    class Meta:
        model = Train
        fields = ("id", "name", "cargo_num", "places_in_cargo", "train_type",)


class TrainRetrieveSerializer(TrainSerializer):
    train_type = TrainTypeSerializer(read_only=True)


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance",)

    def validate(self, attrs):
        Route.validate_route(
            attrs["source"].name,
            attrs["destination"].name
        )
        return attrs


class RouteListSerializer(serializers.ModelSerializer):
    source = serializers.CharField(source="source.name", read_only=True)
    destination = serializers.CharField(source="destination.name", read_only=True)

    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance",)


class RouteRetrieveSerializer(RouteSerializer):
    source = StationSerializer(read_only=True)
    destination = StationSerializer(read_only=True)


class JourneySerializer(serializers.ModelSerializer):
    class Meta:
        model = Journey
        fields = ("id", "route", "train", "departure_time", "arrival_time", "crew",)


class JourneyListSerializer(serializers.ModelSerializer):
    route = serializers.CharField(source="route.route", read_only=True)
    train_name = serializers.CharField(source="train.name", read_only=True)
    train_num_cargo = serializers.CharField(source="train.cargo_num", read_only=True)
    crew = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="full_name"
    )
    tickets_available = serializers.IntegerField(read_only=True)

    class Meta:
        model = Journey
        fields = ("id",
                  "route",
                  "train_name",
                  "train_num_cargo",
                  "departure_time",
                  "arrival_time",
                  "crew",
                  "tickets_available")


class JourneyRetrieveSerializer(JourneySerializer):
    train = TrainRetrieveSerializer(read_only=True)
    route = RouteRetrieveSerializer(read_only=True)
    crew = CrewSerializer(read_only=True, many=True)
    taken_seats = serializers.SerializerMethodField()

    class Meta:
        model = Journey
        fields = ("id", "route", "train", "departure_time", "arrival_time", "crew", "taken_seats",)

    def get_taken_seats(self, obj):
        tickets = Ticket.objects.filter(journey=obj).values_list("cargo", "seat")
        taken_seats = {}
        for cargo, seat in tickets:
            if cargo not in taken_seats:
                taken_seats[cargo] = []
            taken_seats[cargo].append(seat)

        return taken_seats


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("id", "cargo", "seat", "journey",)

    def validate(self, attrs):
        Ticket.validate_ticket(
            attrs["seat"],
            attrs["journey"].train.places_in_cargo,
            attrs["cargo"],
            attrs["journey"].train.cargo_num
        )
        return attrs


class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=False, allow_empty=False)

    class Meta:
        model = Order
        fields = ("id", "created_at", "tickets")

    def create(self, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets")
            order = Order.objects.create(**validated_data)
            for ticket_data in tickets_data:
                Ticket.objects.create(order=order, **ticket_data)

            return order
