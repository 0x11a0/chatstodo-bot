
# @app.on_message(filters.group)
# async def track_user_interaction(client, message):
#     user_id = str(message.from_user.id)  # Convert to string for JSON keys
#     chat_id = message.chat.id
#     # Load existing data
#     try:
#         with open("user_chat_interactions.json", "r") as file:
#             user_chat_interactions = json.load(file)
#     except (FileNotFoundError, json.JSONDecodeError):
#         user_chat_interactions = {}
#         print(user_chat_interactions)

#     # Update the interactions
#     if user_id not in user_chat_interactions:
#         user_chat_interactions[user_id] = []
#     if chat_id not in user_chat_interactions[user_id]:
#         user_chat_interactions[user_id].append(chat_id)

#     # Save back to the file
#     with open("user_chat_interactions.json", "w") as file:
#         json.dump(user_chat_interactions, file, indent=4)


# @app.on_message(filters.group)
# async def handle_message(client, message):
#     user_name = message.from_user.username
#     chat_id = message.chat.id
#     text = message.text or message.caption or ''

#     if f"{chat_id}" in user_messages:
#         user_messages[f"{chat_id}"].append(text)
#     else:
#         user_messages[f"{chat_id}"] = [text]

#     with open("messages.json", "w") as file:
#         json.dump(user_messages, file, indent=4)

#     print(
#         f"User {user_name or message.from_user.id} said: {text}")
