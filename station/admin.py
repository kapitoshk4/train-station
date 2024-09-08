from django.contrib import admin
from station.models import (
    Crew,
    Station,
    Order,
    TrainType,
    Train,
    Route,
    Journey,
    Ticket
)


class TicketInLine(admin.TabularInline):
    model = Ticket
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = (TicketInLine,)


admin.site.register(Crew)
admin.site.register(Station)
admin.site.register(TrainType)
admin.site.register(Train)
admin.site.register(Route)
admin.site.register(Journey)
admin.site.register(Ticket)
