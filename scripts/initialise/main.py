import sys
import asyncio
from pyrogram import Client, filters

import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

app = Client("chats_todo_bot", API_ID, API_HASH, BOT_TOKEN)

app.run(exit())
