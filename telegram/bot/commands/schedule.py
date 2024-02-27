from bot.utils import get_user_groups
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.commands.commands import COMMANDS



async def handle_schedule(client, message):
    command = message.command[0]
    reply = COMMANDS[command]["message"]
    await message.reply_text(reply)