from bot.commands.commands import COMMANDS
from bot.chat_handler import process_chat_history
from api.openai_manager import OpenAiHelper

import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.getcwd(), '.env')
load_dotenv(dotenv_path)

OPENAI_KEY = os.getenv("OPENAI_KEY")
TURN_ON = os.getenv("TURN_ON") == "True"


async def handle_all(client, message):
    command = message.command[0]
    reply = COMMANDS[command]["message"]
    user_id = message.from_user.id

    all_content = await process_chat_history(client, user_id)

    processed_chat = ""

    for chat, content in all_content.items():
        processed_chat += f"<b>{chat}</b>\n\n"

        chat_log = " ".join(content)

        if TURN_ON:
            openai_helper = OpenAiHelper(OPENAI_KEY)
            response = openai_helper.get_summary_event_todo_response(chat_log)
        else:
            response = "mocked overview"

        processed_chat += response + "\n\n"

    response_message = "Here is the overview you requested for!\n\n" + \
        processed_chat
    await message.reply_text(response_message)


async def handle_all_for_a_group(client, message):
    command = message.command[0]
    reply = COMMANDS[command]["message"]
    current_chat_id = message.chat.id
    user_id = message.from_user.id

    all_content = await process_chat_history(client, user_id, current_chat_id)
    chat_log = " ".join(all_content.get(current_chat_id, {}))

    if TURN_ON:
        openai_helper = OpenAiHelper(OPENAI_KEY)
        response = openai_helper.get_summary_event_todo_response(chat_log)
    else:
        response = "mocked overview"

    response_message = "Here is the overview you requested for!\n\n" + response
    await message.reply_text(response_message)
