from django.db.models import Count, F
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

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
from station.serializers import (
    CrewSerializer,
    StationSerializer,
    TrainSerializer,
    TrainTypeSerializer,
    OrderSerializer,
    JourneySerializer,
    TicketSerializer,
    RouteSerializer,
    JourneyListSerializer,
    JourneyRetrieveSerializer,
    RouteListSerializer,
    RouteRetrieveSerializer,
    TrainListSerializer,
    TrainRetrieveSerializer,
    OrderListSerializer
)


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer


class StationViewSet(viewsets.ModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationSerializer


class TrainViewSet(viewsets.ModelViewSet):
    queryset = Train.objects.all()
    serializer_class = TrainSerializer

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.action == "list":
            serializer_class = TrainListSerializer
        if self.action == "retrieve":
            serializer_class = TrainRetrieveSerializer

        return serializer_class

    def get_queryset(self):
        queryset = self.queryset

        if self.action in ("list", "retrieve"):
            queryset = queryset.select_related("train_type")

        return queryset


class TrainTypeViewSet(viewsets.ModelViewSet):
    queryset = TrainType.objects.all()
    serializer_class = TrainTypeSerializer


class OrderSetPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = "page_size"
    max_page_size = 20


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = OrderSetPagination
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)

        if self.action == "list":
            queryset = queryset.prefetch_related("tickets__journey__train", "tickets__journey__crew")

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.action == "list":
            serializer_class = OrderListSerializer

        return serializer_class


class JourneyViewSet(viewsets.ModelViewSet):
    queryset = Journey.objects.all()
    serializer_class = JourneySerializer

    @staticmethod
    def _params_to_int(query_string):
        return [int(str_id) for str_id in query_string.split(",")]

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.action == "list":
            serializer_class = JourneyListSerializer
        if self.action == "retrieve":
            serializer_class = JourneyRetrieveSerializer

        return serializer_class

    def get_queryset(self):
        queryset = self.queryset
        crews = self.request.query_params.get("crews")

        if crews:
            crews = self._params_to_int(crews)
            queryset = queryset.filter(crew__id__in=crews)

        if self.action == "list":
            queryset = (
                queryset
                .select_related("route", "train")
                .prefetch_related("crew", "route__destination", "route__source")
                .annotate(
                    tickets_available=(
                            F("train__places_in_cargo")
                            * F("train__cargo_num")
                            - Count("tickets")
                    )
                )
            ).order_by("id")
        if self.action == "retrieve":
            queryset = (
                queryset
                .select_related("route", "train")
                .prefetch_related("crew", "route__destination", "route__source")
            )

        return queryset.distinct()


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.action == "list":
            serializer_class = RouteListSerializer
        if self.action == "retrieve":
            serializer_class = RouteRetrieveSerializer

        return serializer_class

    def get_queryset(self):
        queryset = self.queryset
        if self.action in ("list", "retrieve"):
            queryset = (
                queryset
                .select_related("source", "destination")
            )

        return queryset
