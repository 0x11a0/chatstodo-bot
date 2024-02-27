# ChatsTodo Bots

### Format

This is the format to follow when sending messages to Kafka.

```json    
{
    "platform":"",
    "sender_user_id":"",
    "group_id":"", // an ID
    "timestamp":"", // in ISO 
    "message": ""
}
```

### Instructions

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
    pip install requirements.txt
    ```

