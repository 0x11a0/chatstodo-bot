import os
from os.path import join, dirname
from dotenv import load_dotenv
import json

import asyncio
from pyrogram import Client, filters
from pyrogram.types import BotCommand


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

GROUP_ID = os.environ.get("GROUP_ID")

user_messages = {}


app = Client("chats_todo_bot")


with open("content/messages.json", "r") as file:
    CONTENT = json.load(file)


@app.on_message(filters.command("start"))
async def handle_start(client, message):
    command = message.command[0]
    reply = CONTENT[command]["message"]
    await message.reply_text(f"Hello, {message.from_user.first_name}!\n\n" + reply)


@app.on_message(filters.command("help"))
async def handle_help(client, message):
    command = message.command[0]
    reply = CONTENT[command]["message"]
    await message.reply_text(reply)


@app.on_message(filters.command("viewgroups"))
async def handle_view_groups(client, message):
    command = message.command[0]
    reply = CONTENT[command]["message"]
    await message.reply_text(reply)


@app.on_message(filters.command("addgroup"))
async def handle_add_group(client, message):
    command = message.command[0]
    reply = CONTENT[command]["message"]
    await message.reply_text(reply)


@app.on_message(filters.command("deletegroup"))
async def handle_delete_group(client, message):
    command = message.command[0]
    reply = CONTENT[command]["message"]
    await message.reply_text(reply)


@app.on_message(filters.command("all"))
async def handle_do_all_actions(client, message):
    command = message.command[0]
    reply = CONTENT[command]["message"]
    error_message = CONTENT[command]["error"]
    null_message = CONTENT[command]["null"]
    current_chat_id = f"{message.chat.id}"

    try:
        if current_chat_id in user_messages:
            await message.reply_text(reply)
            await message.reply_text(str(user_messages[f"{message.chat.id}"]))
        else:
            await message.reply_text(null_message)
    except:
        await message.reply_text(error_message)


@app.on_message(filters.command("summary"))
async def handle_do_summary(client, message):
    command = message.command[0]
    reply = CONTENT[command]["message"]
    error_message = CONTENT[command]["error"]
    null_message = CONTENT[command]["null"]
    current_chat_id = f"{message.chat.id}"

    try:
        if current_chat_id in user_messages:
            await message.reply_text(reply)
            await message.reply_text(str(user_messages[f"{message.chat.id}"]))
        else:
            await message.reply_text(null_message)
    except:
        await message.reply_text(error_message)


@app.on_message(filters.command("todo"))
async def handle_do_todo(client, message):
    command = message.command[0]
    reply = CONTENT[command]["message"]
    error_message = CONTENT[command]["error"]
    null_message = CONTENT[command]["null"]
    current_chat_id = f"{message.chat.id}"

    try:
        if current_chat_id in user_messages:
            await message.reply_text(reply)
            await message.reply_text(str(user_messages[f"{message.chat.id}"]))
        else:
            await message.reply_text(null_message)
    except:
        await message.reply_text(error_message)


@app.on_message(filters.command("event"))
async def handle_do_event(client, message):
    command = message.command[0]
    reply = CONTENT[command]["message"]
    error_message = CONTENT[command]["error"]
    null_message = CONTENT[command]["null"]
    current_chat_id = f"{message.chat.id}"

    try:
        if current_chat_id in user_messages:
            await message.reply_text(reply)
            await message.reply_text(str(user_messages[f"{message.chat.id}"]))
        else:
            await message.reply_text(null_message)
    except:
        await message.reply_text(error_message)


@app.on_message(filters.command("feedback"))
async def handle_do_event(client, message):
    command = message.command[0]
    reply = CONTENT[command]["message"]
    await message.reply_text(reply)


# testing if the bot can read messages
# @app.on_message(filters.group & filters.text)
# async def echo(client, message):
#     await message.reply_text(f"You said {message.text}")


async def set_commands():
    await app.set_bot_commands([
        BotCommand("help", "Get help and instructions on how to use the bot"),
        BotCommand("all", "Get summary, todo and event"),
        BotCommand("viewgroups", "View groups that I am connected to"),
        BotCommand("addgroup", "Add groups to track"),
        BotCommand("deletegroup", "Delete groups from my tracking"),
        BotCommand("summary", "Get summary of group(s)"),
        BotCommand("todo", "Get todo of group(s) "),
        BotCommand("event", "Get event of group(s)"),
        BotCommand("feedback", "Let us know how we can better serve you")
    ])


@app.on_message(filters.group)
async def handle_message(client, message):
    user_name = message.from_user.username
    chat_id = message.chat.id
    text = message.text or message.caption or ''

    if f"{chat_id}" in user_messages:
        user_messages[f"{chat_id}"].append(text)
    else:
        user_messages[f"{chat_id}"] = [text]

    # Optionally, save to file for persistence
    with open("messages.json", "w") as file:
        json.dump(user_messages, file, indent=4)

    print(
        f"User {message.from_user.username or message.from_user.id} said: {text}")


async def main():

    async with app:

        await set_commands()  # Set bot commands
        print("Bot is running...")
        await asyncio.get_event_loop().create_future()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
