# ChatsToDo Bot

## Set up

### Environment

1. Install virtualenv

   ```
   pip install virtualenv
   virtualenv venv
   ```

1. Start virtualenv

   For macOS

   ```
   source ./venv/bin/activate
   ```

   For Windows

   ```
   cd venv/bin
   activate.bat
   ```

1. Install requirements

   ```
   pip install -r requirements.txt
   ```

### Telegram API

1. Obtain your Telegram API.

   Access the following [link](https://core.telegram.org/api/obtaining_api_id) and follow the steps to get your API_ID and API_Hash.

1. Obtain your Bot Token.

   Access the following [link](https://core.telegram.org/bots) to get your BOT_TOKEN.

### .env

To change .env use

```
export TURN_ON=False
echo $TURN_ON
```
