from django.db.models import Case, When, Value, IntegerField

from Restaurant.config import Config as c
from Restaurant.models import RestaurantReservation


def get_ordered_reservations():
    """Order reservations by day and service"""
    reservations = RestaurantReservation.objects.filter(is_active=True)

    ordering_conditions = []
    services = c.get_restaurant_services()

    for idx, (service, _) in enumerate(services):
        condition = When(service=Value(service), then=Value(idx))
        ordering_conditions.append(condition)

    annotated_reservations = reservations.annotate(
        service_order=Case(*ordering_conditions,
                           default=Value(len(services)),
                           output_field=IntegerField()
                           )
    )

    return annotated_reservations.order_by('client_arrived', 'day', 'service_order')
