from discord.ext import commands, tasks # for bot commands and tasks
import discord # for discord API
from dataclasses import dataclass # for dataclass
import datetime # for timestamp
from dotenv import load_dotenv # for environment variables
import os # for environment variables
import json # for json dump
from confluent_kafka import Producer # for kafka producer
import sys # for sys.exit

load_dotenv()  # take environment variables from .env.

# bot env var
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))

# kafka env var
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

# kafka acked definition
def acked(err, msg):
    if err is not None:
        print(f"Failed to deliver message: {err.str()}")
    else:
        print(f"Message produced: {msg.topic()}")

# define the prefix for the bot commands
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

# ------------------------------------------------- DISCORD EVENTS -----------------------------------------------------

# BOT READY CHECKS
@bot.event
async def on_ready():
    # send message to console when bot is ready
    print('Logged in as')
    print(bot.user.name)
    print('Console Check: ChatsTodo Bot is Ready')
    
    # send message to channel when bot is ready
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send('Hello! I am ChatsTodo Bot. I am here to help you with your tasks.\n'
                        'Here are the commands you can use:\n'
                        '!ping - Pong!\n')
    
# MESSAGE LISTENER TO KAFKA
@bot.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author.id == bot.user.id:
        return
    
    # check if message is a command, if so return
    if message.content.startswith('!'):
        return
    
    # this line is important for bot commands to work, 
    # otherwise it will not recognise commands as
    # it will not process them and only reads the message
    await bot.process_commands(message)

    # send message to kafka
    platform = "discord"
    sender_user_id = message.author.name
    group_id = message.channel.id
    timestamp = message.created_at.strftime("%Y-%m-%d %H:%M:%S")
    message = message.content
    
    kafka_parcel = {"platform": platform, "sender_user_id": sender_user_id, "group_id": group_id, "timestamp": timestamp, "message": message}
    kafka_parcel_string = json.dumps(kafka_parcel)
    print(kafka_parcel_string) # print the kafka parcel string for debugging
    
    try:
        producer.produce(topic, kafka_parcel_string, callback=acked)
        producer.poll(1) 
    except Exception as e:
        print(f"Error producing message: {e}")
        # sys.exit(f"Error producing message: {e}")

    producer.flush()

# ------------------------------------------------- DISCORD COMMANDS -----------------------------------------------------

# ping command
@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')
    

# run the bot with the provided token
bot.run(BOT_TOKEN)