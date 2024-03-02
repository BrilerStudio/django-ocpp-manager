import aio_pika

from app.queue import get_channel, get_connection, get_exchange


async def publish(data: str, to: str, priority=None, try_count: int = 0) -> None:
    connection = await get_connection()
    channel = await get_channel(connection, to)
    exchange = await get_exchange(channel, to)

    try:
        await exchange.publish(
            aio_pika.Message(
                bytes(data, 'utf-8'),
                content_type='json',
                priority=priority,
            ),
            routing_key=to,
        )
    except:
        if try_count < 5:
            return await publish(data, to, priority, try_count + 1)
        raise
