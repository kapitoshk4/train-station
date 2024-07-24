from rest_framework import viewsets

from station.models import (
    Crew,
    Station,
    Train,
    Order,
    Journey,
    Ticket,
    Route,
    TrainType
)
from station.serializers import CrewSerializer, StationSerializer, TrainSerializer, TrainTypeSerializer, \
    OrderSerializer, JourneySerializer, TicketSerializer, RouteSerializer, JourneyListSerializer, \
    JourneyRetrieveSerializer, RouteListSerializer, RouteRetrieveSerializer, TrainListSerializer, \
    TrainRetrieveSerializer


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer


class StationViewSet(viewsets.ModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationSerializer


class TrainViewSet(viewsets.ModelViewSet):
    queryset = Train.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return TrainListSerializer
        if self.action == "retrieve":
            return TrainRetrieveSerializer

        return TrainSerializer

    def get_queryset(self):
        queryset = self.queryset
        if self.action in ("list", "retrieve"):
            return queryset.select_related("train_type")

        return queryset


class TrainTypeViewSet(viewsets.ModelViewSet):
    queryset = TrainType.objects.all()
    serializer_class = TrainTypeSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class JourneyViewSet(viewsets.ModelViewSet):
    queryset = Journey.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return JourneyListSerializer
        if self.action == "retrieve":
            return JourneyRetrieveSerializer

        return JourneySerializer

    def get_queryset(self):
        queryset = self.queryset
        if self.action in ("list", "retrieve"):
            return queryset.select_related("route", "train").prefetch_related("crew")


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return RouteListSerializer
        if self.action == "retrieve":
            return RouteRetrieveSerializer

        return RouteSerializer

    def get_queryset(self):
        queryset = self.queryset
        if self.action in ("list", "retrieve"):
            return queryset.select_related("source", "destination")

        return queryset
