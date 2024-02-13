import json


def is_authorised(chat_id, username):
    authorised_list = []
    try:
        with open("./authorised_users.json", "r") as file:
            authorised_list = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("File not found")
        return False

    if str(chat_id) in authorised_list:
        return True

    print(f"{chat_id}:{username} is not authorised.")
    return False
