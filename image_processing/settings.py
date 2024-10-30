from os import getenv

MQ_HOST = getenv('MQ_HOST', 'rabbitmq')
MQ_PORT = int(getenv('MQ_PORT', 5672))

MQ_USER = getenv('MQ_USER', 'guest')
MQ_PASS = getenv('MQ_PASS', 'guest')

MQ_EXCHANGE = getenv('MQ_EXCHANGE', '')
MQ_ROUTING_KEY = getenv('MQ_ROUTING_KEY', 'messages')
