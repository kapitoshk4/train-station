from django.urls import path, include
from rest_framework import routers

from station.views import (
    CrewViewSet,
    StationViewSet,
    TrainViewSet,
    OrderViewSet,
    JourneyViewSet,
    TicketViewSet,
    RouteViewSet,
    TrainTypeViewSet
)

router = routers.DefaultRouter()
router.register("crew", CrewViewSet)
router.register("stations", StationViewSet)
router.register("trains", TrainViewSet)
router.register("train-types", TrainTypeViewSet)
router.register("orders", OrderViewSet)
router.register("journeys", JourneyViewSet)
router.register("tickets", TicketViewSet)
router.register("routes", RouteViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "station"
