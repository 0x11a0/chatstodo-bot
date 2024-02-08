import os
from os.path import join, dirname
from dotenv import load_dotenv
import json

import asyncio
from pyrogram import Client, filters
from pyrogram.types import BotCommand, InlineKeyboardMarkup, InlineKeyboardButton


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

GROUP_ID = os.environ.get("GROUP_ID")

user_messages = {}


app = Client("chats_todo_bot")


with open("content/commands.json", "r") as file:
    COMMANDS = json.load(file)


with open("content/submessages.json", "r") as file:
    SUB_MESSAGES = json.load(file)


async def get_user_groups(user_id):
    # Placeholder for your database query
    # Return a list of tuples (group_id, group_name) for the given user_id
    return [(1, "Group A"), (2, "Group B")]  # Example data


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


@app.on_message(filters.command("viewgroups"))
async def handle_view_groups(client, message):
    command = message.command[0]
    reply = COMMANDS[command]["message"]
    await message.reply_text(reply)


@app.on_message(filters.command("addgroup"))
async def handle_add_group(client, message):
    command = message.command[0]
    reply = COMMANDS[command]["message"]
    await message.reply_text(reply)


@app.on_message(filters.command("deletegroup"))
async def handle_delete_group(client, message):
    command = message.command[0]
    reply = COMMANDS[command]["message"]
    await message.reply_text(reply)


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


@app.on_message(filters.command("summary"))
async def handle_do_summary(client, message):
    command = message.command[0]
    reply = COMMANDS[command]["message"]
    error_message = COMMANDS[command]["error"]
    null_message = COMMANDS[command]["null"]
    current_chat_id = f"{message.chat.id}"

    user_id = message.from_user.id
    user_groups = await get_user_groups(user_id)

    # Generate dynamic inline keyboard based on user groups
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton(group_name, callback_data=f"summary_{group_id}")] for group_id, group_name in user_groups] +
        # Optional 'All' button
        [[InlineKeyboardButton("All", callback_data="summary_all")]]
    )

    await message.reply_text("Which groups' summary do you want to view?", reply_markup=keyboard)


# Callback query handler for the summary options
@app.on_callback_query(filters.regex(r"^summary_"))
async def summary_selection(client: Client, callback_query):
    data = callback_query.data
    if data == "summary_all":
        # Handle 'All' selection
        await callback_query.message.edit_text("Here is the summary for all groups!")
    else:
        # Handle specific group selection
        group_id = data.split("_")[1]
        # Retrieve and send the summary for the selected group
        # This part depends on how you store and retrieve summaries for groups
        await callback_query.message.edit_text(f"Here is the summary for Group ID {group_id}")
    # try:
    #     if current_chat_id in user_messages:
    #         await message.reply_text(reply)
    #         await message.reply_text(str(user_messages[f"{message.chat.id}"]))
    #     else:
    #         await message.reply_text(null_message)
    # except:
    #     await message.reply_text(error_message)


@app.on_message(filters.command("todo"))
async def handle_do_todo(client, message):
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


@app.on_message(filters.command("event"))
async def handle_do_event(client, message):
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


@app.on_message(filters.command("feedback"))
async def handle_do_event(client, message):
    command = message.command[0]
    reply = COMMANDS[command]["message"]
    await message.reply_text(reply)


@app.on_message(filters.command("schedule"))
async def handle_do_schedule(client, message):
    command = message.command[0]
    reply = COMMANDS[command]["message"]
    await message.reply_text(reply)


# testing if the bot can read messages
# @app.on_message(filters.group & filters.text)
# async def echo(client, message):
#     await message.reply_text(f"You said {message.text}")


async def set_commands():
    try:
        commands = []
        for command in COMMANDS:
            commands.append(BotCommand(
                command, COMMANDS[command]["description"]))
        await app.set_bot_commands(commands)
        print("Commands set successfully.")
    except Exception as e:
        print(f"Failed to set commands: {e}")


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

        await set_commands()  # Set bot commands
        print("Bot is running...")
        await asyncio.get_event_loop().create_future()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
