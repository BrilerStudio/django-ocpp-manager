from manager.models import Location, Transaction, ChargePoint


async def get_counters():
    locations_count = await Location.objects.acount()
    transactions_count = await Transaction.objects.acount()
    stations_count = await ChargePoint.objects.acount()

    return {
        'locations': locations_count,
        'transactions': transactions_count,
        'stations': stations_count
    }
