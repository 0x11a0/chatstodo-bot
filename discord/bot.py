from discord.ext import commands, tasks # for bot commands and tasks
import discord # for discord API
from dataclasses import dataclass # for dataclass
import datetime # for timestamp
from dotenv import load_dotenv # for environment variables
import os # for environment variables

load_dotenv()  # take environment variables from .env.

BOT_TOKEN = os.getenv('BOT_TOKEN')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))
MAX_SESSION_TIME_MINUTES = 1

@dataclass
class Session:
    is_active: bool = False
    start_time: int = 0


bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

session = Session()



# STARTUP
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print('Console Check: ChatsTodo Bot is Ready')
    
    # send message to channel when bot is ready
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send('Channel Check: ChatsTodo Bot is Ready')


# COMMANDS
# hello command
@bot.command()
async def hello(ctx): # whatever you name this function is the command to type in e.g '!' + 'hello'
    await ctx.send('Hello! I am ChatsTodo Bot. I am here to help you with your tasks.\n'
               'Here are the commands you can use:\n'
               '!ping - Pong!\n'
               '!echo - Echoes your message\n'
               '!add - Adds numbers together\n'
               '!start - Starts a timed session\n'
               '!end - Ends a timed session')
    
# ping command
@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')
    
# echo command
@bot.command()
async def echo(ctx, *, message):
    await ctx.send(message)

# math command
@bot.command()
async def add(ctx, *arr):
    result = 0
    for i in arr:
        result += int(i)
        
    await ctx.send(f" Result = {result}")
    
# start a session command (uses dataclass and timestamp)
@bot.command()
async def start(ctx):
    if session.is_active:
        await ctx.send('Session is already active')
    else:
        session.is_active = True
        session.start_time = ctx.message.created_at.timestamp()
        human_readable_time = ctx.message.created_at.strftime("%d %b %Y %H:%M:%S")
        break_reminder.start()
        await ctx.send(f"New session has started at {human_readable_time}")
        
# end a session command   
@bot.command()
async def end(ctx):
    if session.is_active:
        session.is_active = False
        end_time = ctx.message.created_at.timestamp()
        elapsed_time = end_time - session.start_time
        human_readable_time = str(datetime.timedelta(seconds=elapsed_time))
        break_reminder.stop()
        await ctx.send(f"Session has ended. Elapsed time: {human_readable_time}")
    else:
        await ctx.send('No active session to end')
        
@tasks.loop(minutes=MAX_SESSION_TIME_MINUTES, count=2) # 2 means 2 iterations, however we ignore the first iteration
async def break_reminder():
    
    if break_reminder.current_loop == 0: # first iteration, ignore
        return
    
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send(f'**You have been working for {MAX_SESSION_TIME_MINUTES} minutes**. Take a break!')

    
bot.run(BOT_TOKEN)