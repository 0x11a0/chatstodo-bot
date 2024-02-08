import os
from os.path import join, dirname
from dotenv import load_dotenv
import json

import asyncio
from pyrogram import Client, filters
from bot.commands import summary, todo, event, feedback, schedule, group
from bot.commands.commands import COMMANDS, set_commands


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

GROUP_ID = os.environ.get("GROUP_ID")

user_messages = {}


app = Client("chats_todo_bot")


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


app.on_message(filters.command("groups"))(group.handle_manage_groups)


@app.on_message(filters.command("all"))
async def handle_do_all_actions(client, message):
    command = message.command[0]
    reply = COMMANDS[command]["message"]
    error_message = COMMANDS[command]["error"]
    null_message = COMMANDS[command]["null"]
    current_chat_id = f"{message.chat.id}"

    try:
        if current_chat_id in user_messages:
            await message.reply_text(reply)
            await message.reply_text(str(user_messages[f"{message.chat.id}"]))
        else:
            await message.reply_text(null_message)
    except:
        await message.reply_text(error_message)


app.on_message(filters.command("start"))(handle_start)

app.on_message(filters.command("summary"))(summary.handle_summary)
app.on_callback_query(filters.regex(r"^summary_"))(
    summary.handle_summary_selection)


app.on_message(filters.command("todo"))(todo.handle_todo)
app.on_callback_query(filters.regex(r"^todo_"))(todo.handle_todo_selection)


app.on_message(filters.command("event"))(event.handle_event)
app.on_callback_query(filters.regex(r"^event_"))(event.handle_event_selection)


app.on_message(filters.command("feedback"))(feedback.handle_feedback)


app.on_message(filters.command("schedule"))(schedule.handle_schedule)


# testing if the bot can read messages
# @app.on_message(filters.group & filters.text)
# async def echo(client, message):
#     await message.reply_text(f"You said {message.text}")


@app.on_message(filters.group)
async def handle_message(client, message):
    user_name = message.from_user.username
    chat_id = message.chat.id
    text = message.text or message.caption or ''

    if f"{chat_id}" in user_messages:
        user_messages[f"{chat_id}"].append(text)
    else:
        user_messages[f"{chat_id}"] = [text]

    with open("messages.json", "w") as file:
        json.dump(user_messages, file, indent=4)

    print(
        f"User {user_name or message.from_user.id} said: {text}")


async def main():

    async with app:
        await set_commands(app)  # Set bot commands
        print("Bot is running...")
        await asyncio.get_event_loop().create_future()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
