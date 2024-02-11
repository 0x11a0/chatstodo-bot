from bot.commands.commands import COMMANDS
from bot.chat_handler import process_chat_history
from api.openai_manager import OpenAiHelper

from dotenv import load_dotenv
import os

# Load the environment variables from the .env file
load_dotenv()

OPENAI_KEY = os.getenv("OPENAI_KEY")
TURN_ON = os.getenv("TURN_ON") == "True"


async def handle_task(client, message):
    command = message.command[0]
    reply = COMMANDS[command]["message"]
    user_id = message.from_user.id

    task_content = await process_chat_history(client, user_id)

    processed_chat = ""

    for chat, content in task_content.items():
        processed_chat += f"<b>{chat}</b>\n"

        chat_log = " ".join(content)

        if TURN_ON:
            openai_helper = OpenAiHelper(OPENAI_KEY)
            response = openai_helper.get_task_response(chat_log)
        else:
            response = "mocked tasks"

        processed_chat += f"<b>{chat}</b>\n\n" + response

    response_message = "Here is the task you requested for!\n\n" + \
        processed_chat
    await message.reply_text(response_message)


async def handle_task_for_a_group(client, message):
    command = message.command[0]
    reply = COMMANDS[command]["message"]
    current_chat_id = message.chat.id
    user_id = message.from_user.id

    task_content = await process_chat_history(client, user_id, current_chat_id)
    chat_log = " ".join(task_content.get(current_chat_id, {}))
    print(os.environ.get("TURN_ON"), TURN_ON)
    if TURN_ON:
        openai_helper = OpenAiHelper(OPENAI_KEY)
        response = openai_helper.get_task_response(chat_log)
    else:
        response = "mocked tasks"

    response_message = "Here is the task you requested for!\n\n" + response
    await message.reply_text(response_message)
