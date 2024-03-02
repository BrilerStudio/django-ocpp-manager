from django.db.models import Model

from manager.models import AuditLog


async def audit_log(
    charge_point: Model,
    action: str = None,
    data: any = None,
):
    return await AuditLog.objects.acreate(
        action=(action or '')[:80],
        data=data,
        charge_point=charge_point,
    )
