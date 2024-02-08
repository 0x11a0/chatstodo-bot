from pyrogram.types import BotCommand
import json

with open("content/commands.json", "r") as file:
    COMMANDS = json.load(file)


async def set_commands(app):
    try:
        commands = []
        for command in COMMANDS:
            commands.append(BotCommand(
                command, COMMANDS[command]["description"]))
        await app.set_bot_commands(commands)
        print("Commands set successfully.")
    except Exception as e:
        print(f"Failed to set commands: {e}")
