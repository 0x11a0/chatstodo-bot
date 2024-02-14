from bot.commands.commands import COMMANDS
import json
from pyrogram.errors import PeerIdInvalid, UserNotParticipant


def read_user_interactions():
    """Read all user interactions from the JSON file."""
    try:
        with open("./user_chat_interactions.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        file = open("./user_chat_interactions.json", 'w')
        file.close()
        return {}


async def track_user_interaction(client, message):
    # Check if the message is a command
    if message.text and message.text.startswith('/'):
        print("Command detected, skipping...")
        return  # Skip adding command messages to interactions

    print(f"listening to {message.chat.id}")
    chat_id = str(message.chat.id)  # Convert to string for JSON keys
    user_chat_interactions = read_user_interactions()

    # Initialize the chat in user_chat_interactions if not present
    if chat_id not in user_chat_interactions:
        user_chat_interactions[chat_id] = []

    # Append the new message to the list of messages for this chat
    user_chat_interactions[chat_id].append(
        (str(message.from_user.first_name) + ": " + message.text) or "nil")

    # Save back to the file
    with open("user_chat_interactions.json", "w") as file:
        json.dump(user_chat_interactions, file, indent=4)


async def user_belongs_to_chat(client, user_id, chat_id):
    try:
        member = await client.get_chat_member(chat_id, user_id)
        return True  # If no exception was raised, the user is a member of the chat
    except UserNotParticipant:
        return False  # The user is not a participant in the chat
    except PeerIdInvalid:
        print("The chat ID or user ID is invalid.")
        return False  # The provided chat ID or user ID is invalid


async def process_chat_history(client, user_id, chat_id=None):
    chats = read_user_interactions()
    summary_content = {}

    # If chat_id is provided, filter for that specific group
    if chat_id:
        if str(chat_id) in chats and await user_belongs_to_chat(client, user_id, chat_id):
            summary_content[chat_id] = chats[str(chat_id)]
    else:
        # Process summary for all groups the user belongs to
        for chat, content in chats.items():
            if await user_belongs_to_chat(client, user_id, chat):
                summary_content[chat] = content

    return summary_content
