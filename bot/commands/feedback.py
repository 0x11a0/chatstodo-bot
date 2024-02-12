from bot.commands.commands import COMMANDS


async def handle_feedback_group(client, message):
    await message.reply_text("Your feedback is invaluable to us. Please tell me more in our private message!")


async def handle_feedback_private(client, message):
    command = message.command[0]
    reply = COMMANDS[command]["message"]
    await message.reply_text(reply)
