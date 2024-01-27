from django.db.models import Count, Q
from passlib.hash import pbkdf2_sha256 as sha256

from charge_point_node.models.status_notification import StatusNotificationEvent
from manager.models import ChargePoint
from manager.views.charge_points import CreateChargPointView, ConnectorView


async def update_connectors(event: StatusNotificationEvent):
    charge_point = await ChargePoint.objects.aget(id=event.charge_point_id)
    connector_data = ConnectorView(status=event.payload.status).dict()
    if event.payload.connector_id == 1:
        charge_point.connectors = {event.payload.connector_id: connector_data}
    else:
        charge_point.connectors.update({event.payload.connector_id: connector_data})
    await charge_point.save()


async def build_charge_points_query(account, search):
    query = ChargePoint.objects.filter(
        location__account=account,
        location__is_active=True,
        is_active=True
    ).order_by('updated_at')

    if search:
        query = query.filter(
            Q(id__icontains=search) |
            Q(status__icontains=search) |
            Q(model__icontains=search) |
            Q(location__address1__icontains=search)
        )
    return query.aall()


async def get_charge_point(charge_point_id):
    return await ChargePoint.objects.aget(id=charge_point_id)


async def create_charge_point(data: CreateChargPointView):
    if data.password:
        data.password = sha256.hash(data.password)
    charge_point = ChargePoint(**data.dict())
    await charge_point.save()
    return charge_point


async def update_charge_point(charge_point_id, data):
    await ChargePoint.objects.filter(id=charge_point_id).aupdate(**data.dict(exclude_unset=True))


async def remove_charge_point(charge_point_id):
    await ChargePoint.objects.filter(id=charge_point_id).adelete()


async def get_statuses_counts(account_id):
    result = await ChargePoint.objects.filter(location__account_id=account_id).values('status').annotate(
        count=Count('status')
    )

    return {item['status'].lower(): item['count'] for item in result}
