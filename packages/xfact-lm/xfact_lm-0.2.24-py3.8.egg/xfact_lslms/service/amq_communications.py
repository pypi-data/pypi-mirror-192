import json
import logging
import os
import pika
from pika.credentials import PlainCredentials


logger = logging.getLogger(__name__)

class CommunicationLayer():

    def __init__(self, args, handle):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(os.getenv("AMQ_HOST", "scheduler.xfact.net"),
                                                                       5672,
                                                                       os.getenv("AMQ_VHOST","lm"),
                                                                       credentials=PlainCredentials(username=os.getenv("AMQ_USERNAME", 'lm'),
                                                                                                    password=os.getenv("AMQ_PASSWORD", 'W2MBec6u')),
                                                                       heartbeat=20000),

                                                  )
        self.channel = self.connection.channel()
        self.handle = handle
        self.queue = args.model_name.split('/')[-1].lower()
        logger.info(f'Using Queue {self.queue}')


    def listen(self):
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue=self.queue, on_message_callback=self.on_request)
        self.channel.start_consuming()

    def on_request(self, ch, method, props, body):
        try:
            message = json.loads(body)

            response = self.handle(message)
            response = json.dumps(response)
            ch.basic_publish(exchange='',
                             routing_key=props.reply_to,
                             properties=pika.BasicProperties(correlation_id= \
                                                                 props.correlation_id,

                                                             expiration='5000'),
                             body=response)

            ch.basic_ack(delivery_tag=method.delivery_tag)
            logger.debug(f"ACK: {method.delivery_tag}")

        except Exception as ex:
            logger.error(str(ex))

            response = json.dumps({
                "error": str(ex)
            })

            ch.basic_publish(exchange='',
                             routing_key=props.reply_to,
                             properties=pika.BasicProperties(correlation_id= \
                                                                 props.correlation_id,

                                                             expiration='5000'),
                             body=response)

            ch.basic_reject(delivery_tag=method.delivery_tag, requeue=False)
