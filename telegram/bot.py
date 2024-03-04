import os
from os.path import join, dirname
from dotenv import load_dotenv
import datetime
import json

from confluent_kafka import Producer  # for kafka producer
from telebot.async_telebot import AsyncTeleBot
import asyncio

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
UPSTASH_KAFKA_SERVER = os.getenv("UPSTASH_KAFKA_SERVER")
UPSTASH_KAFKA_USERNAME = os.getenv('UPSTASH_KAFKA_USERNAME')
UPSTASH_KAFKA_PASSWORD = os.getenv('UPSTASH_KAFKA_PASSWORD')

topic = 'chat-messages'
conf = {
    'bootstrap.servers': UPSTASH_KAFKA_SERVER,
    'sasl.mechanisms': 'SCRAM-SHA-256',
    'security.protocol': 'SASL_SSL',
    'sasl.username': UPSTASH_KAFKA_USERNAME,
    'sasl.password': UPSTASH_KAFKA_PASSWORD
}

producer = Producer(**conf)


# kafka acked definition
def acked(err, msg):
    if err is not None:
        print(f"Failed to deliver message: {err.str()}")
    else:
        print(f"Message produced: {msg.topic()}")


bot = AsyncTeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
async def start_message(message):
    await bot.send_message(message.chat.id, 'Hello!')


@bot.message_handler(func=lambda message: message.chat.type in ["group", "supergroup"])
async def listen_to_group_messages(message):
    kafka_parcel = {
        "platform": "Telegram",
        "sender_user_id": message.from_user.id,
        "group_id": message.chat.id,
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "message": message.text
    }

    kafka_parcel_string = json.dumps(kafka_parcel)
    print(kafka_parcel_string)  # print the kafka parcel string for debugging

    try:
        producer.produce(topic, kafka_parcel_string, callback=acked)
        producer.poll(1)
    except Exception as e:
        print(f"Error producing message: {e}")
        # need to handle if cannot send to kafka what to do,
        # now it is an infinite loop that keeps trying to send to kafka
        # sys.exit(f"Error producing message: {e}")

    producer.flush()


async def main():
    print("Bot is running")
    await asyncio.gather(bot.infinity_polling())


if __name__ == '__main__':
    asyncio.run(main())
