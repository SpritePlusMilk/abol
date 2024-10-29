import logging
from typing import TYPE_CHECKING

import pika
from django.conf import settings
from pika.adapters.blocking_connection import BlockingConnection

if TYPE_CHECKING:
    from pika.channel import Channel
    from pika.spec import BasicProperties
    from pika.spec.Basic import Deliver


logger = logging.getLogger(__name__)
logging.basicConfig(filename='./logs/image_processing.log', level=logging.INFO)


def get_connection() -> BlockingConnection:
    return pika.BlockingConnection(
        pika.ConnectionParameters(
            host=settings.MQ_HOST,
            port=settings.MQ_PORT,
            credentials=pika.PlainCredentials(settings.MQ_USER, settings.MQ_PASS),
        )
    )


def produce_message(message: str) -> None:
    with get_connection() as connection, connection.channel() as channel:
        channel.queue_declare(queue=settings.MQ_ROUTING_KEY)
        channel.basic_publish(
            exchange=settings.MQ_EXCANGE, routing_key=settings.MQ_ROUTING_KEY, body=str.encode(message)
        )


def process_message(
    channel: 'Channel',
    method: 'Deliver',
    properties: 'BasicProperties',
    body: bytes,
) -> None:
    print(body)
    logger.info(body)
    channel.basic_ack(delivery_tag=method.delivery_tag)


def consume_message(channel: 'Channel') -> None:
    channel.basic_consume(queue=settings.MQ_ROUTING_KEY, on_message_callback=process_message)
    channel.start_consuming()
