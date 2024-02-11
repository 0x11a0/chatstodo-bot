import json
from pyrogram.errors import PeerIdInvalid, UserNotParticipant


def read_user_interactions():
    """Read all user interactions from the JSON file."""
    try:
        with open("user_chat_interactions.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


async def track_user_interaction(client, message):
    print("listening")
    chat_id = str(message.chat.id)  # Convert to string for JSON keys
    user_chat_interactions = read_user_interactions()

    # Initialize the chat in user_chat_interactions if not present
    if chat_id not in user_chat_interactions:
        user_chat_interactions[chat_id] = []

    # Append the new message to the list of messages for this chat
    user_chat_interactions[chat_id].append(message.text or "Non-text message")

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
