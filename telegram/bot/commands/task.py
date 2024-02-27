from bot.commands.commands import COMMANDS
from bot.chat_handler import process_chat_history


async def handle_task(client, message):
    command = message.command[0]
    reply = COMMANDS[command]["message"]
    user_id = message.from_user.id

    task_content = await process_chat_history(client, user_id)

    processed_chat = ""

    for chat, content in task_content.items():
        processed_chat += f"<b>{chat}</b>\n"
        for line in content:
            processed_chat += f"{line}\n"

    response_message = "Here is the task you requested for!\n\n" + \
        processed_chat
    await message.reply_text(response_message)


async def handle_task_for_a_group(client, message):
    command = message.command[0]
    reply = COMMANDS[command]["message"]
    current_chat_id = message.chat.id
    user_id = message.from_user.id

    task_content = await process_chat_history(client, user_id, current_chat_id)

    processed_chat = ""
    for content in task_content.get(current_chat_id, {}):
        processed_chat += f"{content}\n"

    response_message = "Here is the task you requested for!\n\n" + processed_chat
    await message.reply_text(response_message)