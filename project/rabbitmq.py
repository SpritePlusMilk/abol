import pika
from django.conf import settings
from pika.adapters.blocking_connection import BlockingConnection


def get_connection() -> BlockingConnection:
    return pika.BlockingConnection(
        pika.ConnectionParameters(
            host=settings.MQ_HOST,
            port=settings.MQ_PORT,
            credentials=pika.PlainCredentials(settings.MQ_USER, settings.MQ_PASS),
        )
    )


def produce_message(message: str) -> None:
    if not settings.DEBUG:
        with get_connection() as connection, connection.channel() as channel:
            channel.queue_declare(queue=settings.MQ_ROUTING_KEY)
            channel.basic_publish(
                exchange=settings.MQ_EXCHANGE, routing_key=settings.MQ_ROUTING_KEY, body=str.encode(message)
            )
