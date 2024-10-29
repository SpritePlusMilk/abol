import logging
from typing import TYPE_CHECKING

from django.conf import settings
from retry import retry

from project.rabbitmq import consume_message, get_connection

if TYPE_CHECKING:
    from pika.exceptions import AMQPConnectionError

logger = logging.getLogger(__name__)


@retry(AMQPConnectionError, delay=5)
def consume() -> None:
    with get_connection() as connection, connection.channel() as channel:
        channel.queue_declare(queue=settings.MQ_ROUTING_KEY)
        consume_message(channel)


if __name__ == '__main__':
    logging.basicConfig(filename='./logs/image_processing.log', level=logging.INFO)
    consume()
