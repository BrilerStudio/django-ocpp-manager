from django.db.models import Q

from manager.models import Transaction
from manager.views.transactions import CreateTransactionView, UpdateTransactionView


async def create_transaction(data: CreateTransactionView):
    transaction = Transaction(**data.dict())
    await transaction.asave()
    return transaction


async def update_transaction(transaction_id, data: UpdateTransactionView):
    await Transaction.objects.filter(transaction_id=transaction_id).aupdate(**data.dict())


async def get_transaction(transaction_id):
    return await Transaction.objects.aget(transaction_id=transaction_id)


async def build_transactions_query(account_id, search):
    query = Transaction.objects.filter(account_id=account_id).order_by('-transaction_id')

    if search:
        query = query.filter(
            Q(city__icontains=search) |
            Q(address__icontains=search) |
            Q(vehicle__icontains=search) |
            Q(charge_point__icontains=search)
        )
    return query.aall()
