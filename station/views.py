from django.db.models import Count, F
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter, extend_schema_field
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

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
    OrderListSerializer,
    TrainImageSerializer
)


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer

    @extend_schema(summary="Get list of crews",
                   description="Returns a list of all crew members.")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Retrieve a crew member",
        description="Returns a details of a single crew member by ID."
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Create a new crew member",
        description="Creates a new crew member."
    )
    def create(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Update a crew member",
        description="Updates an existing crew member with the provided data."
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Partial update of a crew member",
        description="Partially updates an existing crew member"
                    "with the provided data."
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        summary="Delete a crew member",
        description="Deletes an existing crew member by ID."
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class StationViewSet(viewsets.ModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationSerializer

    @extend_schema(
        summary="Get list of stations",
        description="Returns a list of all stations."
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Retrieve a station",
        description="Returns a details of a station by ID."
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Create a new station",
        description="Creates a new station."
    )
    def create(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Update a station",
        description="Updates an existing station with the provided data."
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Partial update of a station",
        description="Partially updates an existing station"
                    "with the provided data."
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        summary="Delete a station",
        description="Deletes an existing station by ID."
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class TrainViewSet(viewsets.ModelViewSet):
    queryset = Train.objects.all()
    serializer_class = TrainSerializer

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.action == "list":
            serializer_class = TrainListSerializer
        if self.action == "retrieve":
            serializer_class = TrainRetrieveSerializer
        if self.action == "upload_image":
            serializer_class = TrainImageSerializer

        return serializer_class

    def get_queryset(self):
        queryset = self.queryset
        train_type = self.request.query_params.get("train-type")

        if train_type:
            queryset = queryset.filter(train_type__name=train_type)

        if self.action in ("list", "retrieve"):
            queryset = queryset.select_related("train_type")

        return queryset

    @action(
        methods=["POST"],
        detail=True,
        url_path="upload-image"
    )
    def upload_image(self, request, pk=None):
        train = self.get_object()
        serializer = self.get_serializer(train, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "train-type",
                type={"type": "string"},
                description="Filter by train type (ex. ?train-type=InterCity)"
            )
        ],
        summary="Get list of trains",
        description="Returns list of all trains."
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Retrieve train details",
        description="Returns details of a train by ID."
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(self, request, *args, **kwargs)

    @extend_schema(
        summary="Create a new train",
        description="Creates a new train."
    )
    def create(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Update a train",
        description="Update a train by ID."
    )
    def update(self, request, *args, **kwargs):
        return super().update(self, request, *args, **kwargs)

    @extend_schema(
        summary="Partial update of a train",
        description="Partially updates an existing train"
                    "with the provided data."
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        summary="Delete a train",
        description="Deletes an existing train by ID."
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class TrainTypeViewSet(viewsets.ModelViewSet):
    queryset = TrainType.objects.all()
    serializer_class = TrainTypeSerializer

    @extend_schema(
        summary="Get list of train types",
        description="Returns list of all train types."
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Retrieve train type details",
        description="Returns details of a train type by ID."
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(self, request, *args, **kwargs)

    @extend_schema(
        summary="Create a new train type",
        description="Creates a new train type."
    )
    def create(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Update a train type",
        description="Update a train type by ID."
    )
    def update(self, request, *args, **kwargs):
        return super().update(self, request, *args, **kwargs)

    @extend_schema(
        summary="Partial update of a train type",
        description="Partially updates an existing train type"
                    "with the provided data."
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        summary="Delete a train type",
        description="Deletes an existing train type by ID."
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


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

    @extend_schema(
        summary="Get list of orders",
        description="Returns list of all orders."
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Retrieve order details",
        description="Returns details of a order by ID."
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(self, request, *args, **kwargs)

    @extend_schema(
        summary="Create a new order",
        description="Creates a new order."
    )
    def create(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Update a order",
        description="Update a order by ID."
    )
    def update(self, request, *args, **kwargs):
        return super().update(self, request, *args, **kwargs)

    @extend_schema(
        summary="Partial update of a order",
        description="Partially updates an existing order"
                    "with the provided data."
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        summary="Delete a order",
        description="Deletes an existing order by ID."
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


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

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "crews",
                type={"array": "list", "items": {"type": "number"}},
                description="Filter by crews (ex. ?crews=1,2)"
            )
        ],
        summary="Get list of journeys",
        description="Returns list of all journeys."
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Retrieve journey details",
        description="Returns details of a journey by ID."
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(self, request, *args, **kwargs)

    @extend_schema(
        summary="Create a new journey",
        description="Creates a new journey."
    )
    def create(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Update a journey",
        description="Update a journey by ID."
    )
    def update(self, request, *args, **kwargs):
        return super().update(self, request, *args, **kwargs)

    @extend_schema(
        summary="Partial update of a journey",
        description="Partially updates an existing journey"
                    "with the provided data."
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        summary="Delete a journey",
        description="Deletes an existing journey by ID."
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


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
        source = self.request.query_params.get("source")
        destination = self.request.query_params.get("destination")

        if source:
            queryset = queryset.filter(source__name=source)

        if destination:
            queryset = queryset.filter(destination__name=destination)

        if self.action in ("list", "retrieve"):
            queryset = (
                queryset
                .select_related("source", "destination")
            )

        return queryset
