from bot.commands.commands import COMMANDS
from bot.chat_handler import process_chat_history
from api.t5_task import run_task_model_async
from api.openai_manager import OpenAiHelper

import os
from os.path import join, dirname
from dotenv import load_dotenv


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

OPENAI_KEY = os.environ.get("OPENAI_KEY")


async def handle_task(client, message):
    command = message.command[0]
    reply = COMMANDS[command]["message"]
    user_id = message.from_user.id

    task_content = await process_chat_history(client, user_id)

    processed_chat = ""

    for chat, content in task_content.items():
        processed_chat += f"<b>{chat}</b>\n"

        chat_log = " ".join(content)

        openai_helper = OpenAiHelper(OPENAI_KEY)
        response = openai_helper.get_task_response(chat_log)

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

    openai_helper = OpenAiHelper(OPENAI_KEY)
    response = openai_helper.get_task_response(chat_log)

    response_message = "Here is the task you requested for!\n\n" + response
    await message.reply_text(response_message)
