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


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()


class StationViewSet(viewsets.ModelViewSet):
    queryset = Station.objects.all()


class TrainViewSet(viewsets.ModelViewSet):
    queryset = Train.objects.all()


class TrainTypeViewSet(viewsets.ModelViewSet):
    queryset = TrainType.objects.all()


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()


class JourneyViewSet(viewsets.ModelViewSet):
    queryset = Journey.objects.all()


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
