from bot.commands.commands import COMMANDS


async def handle_feedback(client, message):
    print("feedback")
    command = message.command[0]
    reply = COMMANDS[command]["message"]
    await message.reply_text(reply)
