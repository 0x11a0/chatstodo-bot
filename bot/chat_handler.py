import json

# @app.on_message(filters.group)


async def track_user_interaction(client, message):
    user_id = str(message.from_user.id)  # Convert to string for JSON keys
    chat_id = message.chat.id
    # Load existing data
    try:
        with open("user_chat_interactions.json", "r") as file:
            user_chat_interactions = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        user_chat_interactions = {}
        print(user_chat_interactions)

    # Update the interactions
    if user_id not in user_chat_interactions:
        user_chat_interactions[user_id] = []
    if chat_id not in user_chat_interactions[user_id]:
        user_chat_interactions[user_id].append(chat_id)

    # Save back to the file
    with open("user_chat_interactions.json", "w") as file:
        json.dump(user_chat_interactions, file, indent=4)
