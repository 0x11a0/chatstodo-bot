from bot.commands.commands import COMMANDS
from bot.chat_handler import read_user_interactions, user_belongs_to_chat


async def handle_summary(client, message):
    command = message.command[0]
    reply = COMMANDS[command]["message"]
    error_message = COMMANDS[command]["error"]
    null_message = COMMANDS[command]["null"]
    current_chat_id = f"{message.chat.id}"

    user_id = message.from_user.id

    chats = read_user_interactions()

    preprocessed_chat = {}

    for chat, content in chats.items():
        if await user_belongs_to_chat(client, user_id, chat):
            print(chat, content)
            preprocessed_chat[chat] = content

    await message.reply_text("Here is the summary you requested for!" + str(preprocessed_chat))


async def handle_summary_for_a_group(client, message):
    command = message.command[0]
    reply = COMMANDS[command]["message"]
    error_message = COMMANDS[command]["error"]
    null_message = COMMANDS[command]["null"]
    current_chat_id = f"{message.chat.id}"

    user_id = message.from_user.id

    chats = read_user_interactions()

    preprocessed_chat = []

    if await user_belongs_to_chat(client, user_id, current_chat_id):
        preprocessed_chat = chats[current_chat_id]

    await message.reply_text("Here is the summary you requested for!" + str(preprocessed_chat))
