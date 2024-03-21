from discord.ext import commands, tasks # for bot commands and tasks
import discord # for discord API
import datetime # for timestamp
from dotenv import load_dotenv # for environment variables
import os # for environment variables
from os.path import join, dirname, exists
import json # for json dump
from confluent_kafka import Producer # for kafka producer
import sys # for sys.exit
import requests # for requests
from db.mongodb import MongoDBHandler # for mongodb

# load the environment variables
load_dotenv()

# bot env var
BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')

# mongodb env var
GROUP_MONGODB_URL = os.getenv('GROUP_MONGODB_URL')

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

groups_db = MongoDBHandler(db_url=GROUP_MONGODB_URL)

# kafka acked definition
def acked(err, msg):
    if err is not None:
        print(f"Failed to deliver message: {err.str()}")
    else:
        print(f"Message produced: {msg.topic()}")

# define the prefix for the bot commands
bot = commands.Bot(command_prefix='/', intents=discord.Intents.all())
# ------------------------------------------------- DISCORD EVENTS -----------------------------------------------------

# BOT READY CHECK ON CONSOLE
@bot.event
async def on_ready():
    # send message to console when bot is ready
    print('Logged in as')
    print(bot.user.name)
    print('Console Check: ChatsTodo Bot is Ready')
    
# MESSAGE LISTENER TO KAFKA
@bot.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author.id == bot.user.id:
        return
    
    # this line is important for bot commands to work, 
    # otherwise it will not recognise commands as
    # it will not process them and only reads the message
    await bot.process_commands(message)
    
    # check if message is a command, if so return
    if message.content.startswith(bot.command_prefix):
        return

    # send message to kafka
    platform = "discord"
    sender_user_id = message.author.name
    group_id = message.channel.id
    timestamp = message.created_at.isoformat()
    message = message.content
    
    kafka_parcel = {"platform": platform, "sender_user_id": sender_user_id, "group_id": group_id, "timestamp": timestamp, "message": message}
    kafka_parcel_string = json.dumps(kafka_parcel)
    print(kafka_parcel_string) # print the kafka parcel string for debugging
    
    try:
        producer.produce(topic, kafka_parcel_string, callback=acked)
        producer.poll(1) 
    except Exception as e:
        print(f"Error producing message: {e}")
        # need to handle if cannot send to kafka what to do,
        # now it is an infinite loop that keeps trying to send to kafka       
        # sys.exit(f"Error producing message: {e}")

    producer.flush()

# ------------------------------------------------- DISCORD COMMANDS -----------------------------------------------------

#ping command
@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')
    
# hi command
@bot.command()
async def hi(ctx):
    await ctx.send('Hello! I am ChatsTodo Bot. I am here to help you with your tasks.\n'
                    'Here are the commands you can use:\n'
                    '!ping - Pong!\n')
    
# connect command
@bot.command()
async def connect(ctx):
    if isinstance(ctx.channel, discord.DMChannel):  # Check if the command is issued in a private channel
        api_url = "http://authentication:8080/auth/api/v1/bot/request-code"
        
        user_credentials = {"userId": str(ctx.author.id), "platform": "Discord"}
        
        response = requests.post(api_url, json=user_credentials)
        
        x = response.json()
        code = x["verification_code"]
        await ctx.send(f"Here is your code {code}")
    
# summary command
@bot.command()
async def summary(ctx):
    if isinstance(ctx.channel, discord.DMChannel):
        await ctx.send('Here is your summary...\n')
        
# track command
@bot.command()
async def track(ctx):
    if isinstance(ctx.guild, discord.Guild):  # Check if the command is issued in a guild
        guild_id = ctx.guild.id
        guild_name = ctx.guild.name
        user_id = ctx.author.id

        guild_data = {
            "user_id": str(user_id),
            "guild_id": str(guild_id),
            "guild_name": str(guild_name),
            "platform": "Discord",
            "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }

        groups_db.insert_group(guild_data)

        # send a pm to the user
        await ctx.author.send(f"You have added '{guild_name}' to your tracking list")
        
# view groups command
async def refresh_groups(user_id, groups_db, bot):
    groups = groups_db.get_groups_of_user(user_id)
    current_groups = []
    print(f"Groups: {groups}")

    # for loop the groups in db and check if the user is still in the group
    # if not, remove the group from the db
    for group in groups:
        group_id = int(group["group_id"])
        print(f"Group ID: {group_id}")
        guild = bot.get_guild(group_id)
        if guild is not None:
            member = guild.get_member(user_id)
            if member is not None:
                group["group_name"] = guild.name
                current_groups.append(group)

                # update the new group name in the db if it is not the same as db
                if guild.name != group["group_name"]:
                    groups_db.update_group(group_id, user_id, guild.name)
            else:
                groups_db.delete_group_of_user(group_id, user_id)

    return current_groups

@bot.command()
async def viewGroups(ctx):
    if isinstance(ctx.channel, discord.DMChannel):  # Check if the command is issued in a private channel
        user_id = ctx.author.id
        current_groups = await refresh_groups(user_id, groups_db, bot)

        if current_groups:
            reply = "Here are the groups you are tracking:\n"
            for group in current_groups:
                reply += f"- {group['group_name']}\n"
        else:
            reply = "You are not tracking any groups yet"

        await ctx.send(reply)
        
# delete group command
@bot.command()
async def deleteGroups(ctx):
    if isinstance(ctx.channel, discord.DMChannel):  # Check if the command is issued in a private channel
        user_id = ctx.author.id
        current_groups = await refresh_groups(user_id, groups_db, bot)

        if not current_groups:
            await ctx.send("You are not tracking any groups yet.")
            return

        for group in current_groups:
            await ctx.send(f"Do you want to remove '{group['group_name']}'? Type '/confirmDelete {group['group_id']}' to confirm.")

@bot.command()
async def confirmDelete(ctx, group_id: int):
    if isinstance(ctx.channel, discord.DMChannel):  # Check if the command is issued in a private channel
        user_id = ctx.author.id

        # Assuming the delete_group_of_user method returns a boolean indicating success
        count = groups_db.delete_group_of_user(
            str(group_id), user_id, platform="Discord")

        if count > 0:
            # Notify the user that the group has been removed
            await ctx.send("Group removed successfully.")
        else:
            await ctx.send("Failed to remove group.")
            
@bot.event
async def on_member_remove(member):
    user_id = member.id
    guild_id = member.guild.id

    # Check if the user and guild ID exist in the database
    group = groups_db.get_group_of_user(str(guild_id), user_id, platform="Discord")

    # If the group exists, delete it
    if group:
        groups_db.delete_group_of_user(str(guild_id), user_id)

# run the bot with the provided token
bot.run(BOT_TOKEN)