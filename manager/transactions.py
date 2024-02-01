from rest_framework import serializers

from manager.models import Transaction, TransactionStatus
from manager.tasks import remote_start_transaction_task, remote_stop_transaction_task


def create_remote_transaction(
        charge_point,
        connector_id,
        vehicle: str = None,
        city: str = None,
        address: str = None,
        external_id: str = None,
        *args,
        **kwargs,
):
    if not charge_point.is_enabled:
        raise serializers.ValidationError({'charge_point_id': 'Charge point is disabled'})

    if not charge_point.is_available(connector_id):
        raise serializers.ValidationError({'connector_id': 'Connector is not available'})

    transaction = Transaction.objects.create(
        city=city or charge_point.location.city if charge_point.location else 'Unknown',
        address=address or charge_point.location.address1 if charge_point.location else 'Unknown',
        vehicle=vehicle or 'Unknown',
        charge_point=charge_point,
        connector_id=connector_id,
        external_id=external_id,
        status=TransactionStatus.initialized.value,
    )

    remote_start_transaction_task.delay(transaction.transaction_id)

    return transaction


def stop_remote_transaction(transaction: Transaction):
    if transaction.status == TransactionStatus.stopped.value:
        raise serializers.ValidationError({'transaction_id': 'Transaction is already stopped'})

    Transaction.objects.filter(
        transaction_id=transaction.transaction_id,
        status=TransactionStatus.started.value,
    ).update(
        status=TransactionStatus.stopping.value,
    )

    remote_stop_transaction_task.delay(transaction.transaction_id)

    transaction.refresh_from_db()

    return transaction
