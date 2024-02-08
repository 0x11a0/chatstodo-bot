from bot.utils import get_user_groups
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.commands.commands import COMMANDS


async def handle_event(client, message):
    command = message.command[0]
    reply = COMMANDS[command]["message"]
    error_message = COMMANDS[command]["error"]
    null_message = COMMANDS[command]["null"]
    current_chat_id = f"{message.chat.id}"

    user_id = message.from_user.id
    user_groups = await get_user_groups(user_id)

    # Generate dynamic inline keyboard based on user groups
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton(group_name, callback_data=f"event_{group_id}")] for group_id, group_name in user_groups] +
        # Optional 'All' button
        [[InlineKeyboardButton("All", callback_data="event_all")]]
    )

    await message.reply_text("Which groups' event do you want to view?", reply_markup=keyboard)


async def handle_event_selection(client, callback_query):
    data = callback_query.data
    if data == "event_all":
        # Handle 'All' selection
        await callback_query.message.edit_text("Here are your events for all groups!")
    else:
        # Handle specific group selection
        group_id = data.split("_")[1]
        # Retrieve and send the summary for the selected group
        # This part depends on how you store and retrieve summaries for groups
        await callback_query.message.edit_text(f"Here are your event for Group ID {group_id}")
    # try:
    #     if current_chat_id in user_messages:
    #         await message.reply_text(reply)
    #         await message.reply_text(str(user_messages[f"{message.chat.id}"]))
    #     else:
    #         await message.reply_text(null_message)
    # except:
    #     await message.reply_text(error_message)
