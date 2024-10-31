import logging
from typing import TYPE_CHECKING

import pika
import settings
from pika.adapters.blocking_connection import BlockingConnection

if TYPE_CHECKING:
    from pika.channel import Channel
    from pika.spec import BasicProperties
    from pika.spec.Basic import Deliver


logger = logging.getLogger(__name__)
logging.basicConfig(filename='image_processing.log', format='%(asctime)s %(message)s', filemode='w', level=logging.INFO)


def get_connection() -> BlockingConnection:
    return pika.BlockingConnection(
        pika.ConnectionParameters(
            host=settings.MQ_HOST,
            port=settings.MQ_PORT,
            credentials=pika.PlainCredentials(settings.MQ_USER, settings.MQ_PASS),
        )
    )


def process_message(
    channel: 'Channel',
    method: 'Deliver',
    properties: 'BasicProperties',
    body: bytes,
) -> None:
    """Callback для логирования сообщения"""
    message = body.decode()
    print(message)
    logger.info(message)
    channel.basic_ack(delivery_tag=method.delivery_tag)


def consume_message(channel: 'Channel') -> None:
    """Функция для приёма сообщения"""
    channel.basic_consume(queue=settings.MQ_ROUTING_KEY, on_message_callback=process_message)
    channel.start_consuming()
