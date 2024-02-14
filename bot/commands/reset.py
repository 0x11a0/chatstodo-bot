import json
from bot.auth import is_authorised

import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


def reset_chat(chat_id):
    user_chat_interactions = {}
    original_chat = {}

    try:
        with open("./user_chat_interactions.json", "r") as file:
            user_chat_interactions = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Error loading user_chat_interactions.json.")
        file = open("./user_chat_interactions.json", 'w')
        file.close()

    try:
        with open("./chat_state.json", "r") as file:
            original_chat = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Error loading chat_state.json.")
        file = open("./chat_state.json", 'w')
        file.close()

    if chat_id in original_chat:
        user_chat_interactions[chat_id] = original_chat[chat_id]
    else:
        print(f"Original chat state {chat_id} not found")

    with open("./user_chat_interactions.json", "w") as file:
        json.dump(user_chat_interactions, file, indent=2)

    return True


async def delete_messages_after_datetime(app, chat_id, datetime_cutoff):
    async for message in app.get_chat_history(chat_id):
        if message.date > datetime_cutoff:
            try:
                # Delete the message
                await app.delete_messages(chat_id, message.message_id)
                print(f"Deleted message {message.message_id}")
            except Exception as e:
                print(
                    f"Could not delete message {message.message_id}: {e}")


async def handle_reset_state(client, message):
    print(message.from_user.id, message.from_user.first_name)
    if is_authorised(message.from_user.id, message.from_user.first_name):
        chat_id = os.getenv("TRACK_RESET_CHAT_ID")
        has_reset = reset_chat(chat_id)
        if has_reset:
            await message.reply_text("Chat history has been successfully reset! Please manually delete up till the dashes")
        else:
            await message.reply_text("There is an issue with resetting. Please contact the admin.")
    else:
        await message.reply_text("You are not authorised to do this action")
