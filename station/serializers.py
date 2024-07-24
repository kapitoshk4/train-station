from rest_framework import serializers

from station.models import Station, Crew, Journey, Route, Train, TrainType, Order, Ticket


class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = ("id", "name", "latitude", "longitude",)


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = ("id", "first_name", "last_name",)


class TrainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Train
        fields = ("id", "name", "cargo_num", "places_in_cargo", "train_type",)


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance",)


class JourneySerializer(serializers.ModelSerializer):
    class Meta:
        model = Journey
        fields = ("id", "route", "train", "departure_time", "arrival_time", "crew",)


class JourneyListSerializer(serializers.ModelSerializer):
    train_name = serializers.CharField(source="train.name", read_only=True)
    train_num_cargo = serializers.CharField(source="train.num_cargo", read_only=True)
    crew = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="full_name"
    )

    class Meta:
        model = Journey
        fields = ("id", "route", "train_name", "train_num_cargo", "departure_time", "arrival_time", "crew",)


class JourneyRetrieveSerializer(JourneySerializer):
    train = TrainSerializer(read_only=True)
    route = RouteSerializer(read_only=True)
    crew = CrewSerializer(read_only=True)


class TrainTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainType
        fields = ("id", "name",)


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("id", "created_at", "user",)


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("id", "cargo", "seat", "journey", "order")
