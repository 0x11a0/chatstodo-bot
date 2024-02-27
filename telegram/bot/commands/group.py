from bot.utils import get_user_groups
from pyrogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from bot.commands.commands import COMMANDS
import re

# Dummy list of groups for demonstration purposes
# 10 groups named Group 1 to Group 10
groups = [f"Group {i}" for i in range(1, 11)]

# Tracking the current page of groups for each user
user_pages = {}


def generate_keyboard(user_id):
    # Determine the current page for the user
    current_page = user_pages.get(user_id, 0)
    # Generate group buttons for the current page
    start_index = current_page * 3
    end_index = start_index + 3
    group_buttons = [[KeyboardButton(group)]
                     for group in groups[start_index:end_index]]

    # Add control buttons
    control_buttons = [
        [KeyboardButton("⬅️ Previous"), KeyboardButton("Next ➡️")],
        [KeyboardButton("Add Groups"), KeyboardButton("Help")],
        [KeyboardButton("Exit")]
    ]

    return ReplyKeyboardMarkup(group_buttons + control_buttons, resize_keyboard=True)


def generate_group_action_keyboard(group_name):
    return ReplyKeyboardMarkup([
        [KeyboardButton(f"Delete {group_name}")],
        [KeyboardButton("Back to Groups")]
    ], resize_keyboard=True)


async def handle_manage_groups(client, message):
    user_id = message.from_user.id
    user_pages[user_id] = 0  # Start from the first page
    keyboard = generate_keyboard(user_id)
    await message.reply_text("Choose a group:", reply_markup=keyboard)


async def handle_group_navigation(client, message):
    user_id = message.from_user.id
    text = message.text

    if text == "Next ➡️":
        user_pages[user_id] = user_pages.get(user_id, 0) + 1
    elif text == "⬅️ Previous":
        user_pages[user_id] = max(user_pages.get(user_id, 0) - 1, 0)
    elif text == "Exit":
        await message.reply_text("Exiting.", reply_markup=ReplyKeyboardRemove())
        return

    keyboard = generate_keyboard(user_id)
    await message.reply_text("Choose a group:", reply_markup=keyboard)


async def handle_individual_group_actions(client, message):
    user_id = message.from_user.id
    text = message.text

    # Assuming "Group " is a prefix for all group names
    if text.startswith("Group "):
        # User has selected a group, show options for this group
        action_keyboard = generate_group_action_keyboard(text)
        await message.reply_text(f"Actions for {text}:", reply_markup=action_keyboard)
    elif text.startswith("Delete "):
        # Handle group deletion
        group_name = text.replace("Delete ", "")
        # Place your deletion logic here
        await message.reply_text(f"{group_name} has been deleted.")
    elif text.startswith("Back "):
        await message.reply_text("Choose a group:", reply_markup=generate_keyboard(user_id))


async def handle_add_group(client, callback_query):
    await callback_query.message.edit_text("Functionality to view groups will be implemented here.")
