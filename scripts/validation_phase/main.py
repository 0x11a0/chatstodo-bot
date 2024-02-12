import json
import sys


def reset_chat(chat_id):
    user_chat_interactions = {}
    original_chat = {}

    try:
        with open("./user_chat_interactions.json", "r") as file:
            user_chat_interactions = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Error loading user_chat_interactions.json.")
        return False

    try:
        with open("./scripts/validation_phase/chat_state.json", "r") as file:
            original_chat = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Error loading chat_state.json.")
        return False  # Return False to indicate failure

    if chat_id in user_chat_interactions and chat_id in original_chat:
        user_chat_interactions[chat_id] = original_chat[chat_id]
    else:
        print(
            f"Chat ID {chat_id} not found in either user_chat_interactions or original_chat.")
        return False

    with open("./user_chat_interactions.json", "w") as file:
        json.dump(user_chat_interactions, file, indent=2)

    return True


if __name__ == "__main__":
    if len(sys.argv) != 2:  # Expect exactly one argument: the script name and the chat_id
        print("Usage: python main.py <chat_id>")
        # Exit the script indicating that the command was used incorrectly
        sys.exit(1)

    # sys.argv[0] is the script name, sys.argv[1] is the first argument passed to the script
    chat_id = sys.argv[1]
    result = reset_chat(chat_id)
    if result:
        print("Chat reset successfully.")
    else:
        print("Failed to reset chat.")
