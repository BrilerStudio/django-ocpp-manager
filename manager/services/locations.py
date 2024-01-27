from django.db.models import Count, Q

from manager.models import Location
from manager.views.locations import CreateLocationView


def criterias(account_id):
    return Q(account_id=account_id, is_active=True)


async def list_simple_locations(account_id):
    return await Location.objects.filter(criterias(account_id)).distinct().all()


async def remove_location(location_id):
    await Location.objects.filter(id=location_id).delete()


async def create_location(account_id, data: CreateLocationView):
    location = Location(account_id=account_id, **data.dict())
    await location.save()
    return location


async def build_locations_query(account_id, search):
    query = Location.objects.filter(criterias(account_id)).annotate(
        charge_points_count=Count('chargepoint')
    ).order_by('-created_at')

    if search:
        query = query.filter(
            Q(name__icontains=search) |
            Q(city__icontains=search) |
            Q(address1__icontains=search)
        )
    return query
