#!/bin/bash

# initialise_session.sh

# Load and export .env variables
export $(grep -v '^#' .env | xargs)

printf '%s\ny\n' "$BOT_TOKEN" | python ./scripts/initialise/main.py | mv chats_todo_bot.session ../../