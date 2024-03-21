from confluent_kafka import Producer
import os
from dotenv import load_dotenv

load_dotenv()

topic = 'chat-messages'
UPSTASH_KAFKA_SERVER = os.getenv("UPSTASH_KAFKA_SERVER")
UPSTASH_KAFKA_USERNAME = os.getenv('UPSTASH_KAFKA_USERNAME')
UPSTASH_KAFKA_PASSWORD = os.getenv('UPSTASH_KAFKA_PASSWORD')

conf = {
    'bootstrap.servers': UPSTASH_KAFKA_SERVER,
    'sasl.mechanisms': 'SCRAM-SHA-256',
    'security.protocol': 'SASL_SSL',
    'sasl.username': UPSTASH_KAFKA_USERNAME,
    'sasl.password': UPSTASH_KAFKA_PASSWORD
}

producer = Producer(**conf)


def acked(err, msg):
    if err is not None:
        print(f"Failed to deliver message: {err.str()}")
    else:
        print(f"Message produced: {msg.topic()}")


try:
    producer.produce(topic, b'Hello from python', callback=acked)
    producer.poll(1) 
except Exception as e:
    print(f"Error producing message: {e}")

producer.flush()
