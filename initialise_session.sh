#!/bin/bash

# initialise_session.sh

# Load and export .env variables
export $(grep -v '^#' .env | xargs)

{
    echo "$BOT_TOKEN"
    echo "y"
} | python ./scripts/initialise/main.py

mv ./scripts/initialise/chats_todo_bot.session ../../