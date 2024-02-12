import os
from os.path import join, dirname
from dotenv import load_dotenv
import json

import asyncio
from pyrogram import Client, filters
from bot.commands import summary, task, event, feedback, schedule, group, all
from bot import chat_handler
from bot.commands.commands import COMMANDS, set_commands


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

OPENAI_KEY = os.environ.get("OPENAI_KEY")
IS_OPENAI_TURN_ON = os.environ.get("TURN_ON")

user_messages = {}


app = Client("chats_todo_bot", api_id=API_ID,
             api_hash=API_HASH, bot_token=BOT_TOKEN)

with open("content/submessages.json", "r") as file:
    SUB_MESSAGES = json.load(file)


@app.on_message(filters.command("start"))
async def handle_start(client, message):
    command = message.command[0]
    reply = COMMANDS[command]["message"]
    await message.reply_text(f"Hello, {message.from_user.first_name}!\n\n" + reply)


@app.on_message(filters.command("help"))
async def handle_help(client, message):
    command = message.command[0]
    reply = COMMANDS[command]["message"]
    await message.reply_text(reply)


app.on_message(filters.group & filters.text, group=1)(
    chat_handler.track_user_interaction)
app.on_message(filters.command("start"))(handle_start)

app.on_message(filters.command("task") & filters.private)(task.handle_task)
app.on_message(filters.command("task") & filters.group)(
    task.handle_task_for_a_group)

app.on_message(filters.command("summary") &
               filters.private)(summary.handle_summary)
app.on_message(filters.command("summary") &
               filters.group)(summary.handle_summary_for_a_group)


app.on_message(filters.command("event") & filters.private)(event.handle_event)
app.on_message(filters.command("event") & filters.group)(
    event.handle_event_for_a_group)


app.on_message(filters.command("all") & filters.private)(all.handle_all)
app.on_message(filters.command("all") & filters.group)(
    all.handle_all_for_a_group)

app.on_message(filters.command("groups"))(group.handle_manage_groups)
app.on_message(filters.text & filters.regex(
    "^(⬅️ Previous|Next ➡️|Add Groups|Help|Exit)$"))(group.handle_group_navigation)
app.on_message(filters.text & ~filters.regex(
    "^(⬅️ Previous|Next ➡️|Add Groups|Help|Exit)$"))(group.handle_individual_group_actions)


app.on_message(filters.command("feedback"))(feedback.handle_feedback)


app.on_message(filters.command("schedule"))(schedule.handle_schedule)


async def main():

    async with app:

        await set_commands(app)  # Set bot commands
        print("Bot is running...")
        await asyncio.get_event_loop().create_future()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
