from os import getenv

from pika.exceptions import AMQPConnectionError
from retry import retry
from tools import consume_message, get_connection

MQ_ROUTING_KEY = getenv('MQ_ROUTING_KEY', 'messages')


@retry(AMQPConnectionError, delay=5)
def consume() -> None:
    with get_connection() as connection, connection.channel() as channel:
        channel.queue_declare(queue=MQ_ROUTING_KEY)
        consume_message(channel)


if __name__ == '__main__':
    consume()
