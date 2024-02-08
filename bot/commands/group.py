from bot.utils import get_user_groups
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.commands.commands import COMMANDS


async def handle_manage_groups(client, message):
    command = message.command[0]
    reply = COMMANDS[command]["message"]
    user_id = message.from_user.id

    await message.reply_text(reply)


async def handle_view_group(client, message):
    command = message.command[0]
    reply = COMMANDS[command]["message"]
    user_id = message.from_user.id
    user_groups = await get_user_groups(user_id)
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton(group_name, callback_data=f"summary_{
                               group_id}")] for group_id, group_name in user_groups]
    )
    await message.reply_text(reply, reply_markup=keyboard)


async def handle_add_group(client, message):
    command = message.command[0]
    reply = COMMANDS[command]["message"]
    await message.reply_text(reply)


async def handle_delete_group(client, message):
    command = message.command[0]
    reply = COMMANDS[command]["message"]
    await message.reply_text(reply)
