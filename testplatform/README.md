# Test platform

### Overview

This is a sample code to refer to when creating new services for different platforms to publish messages to Kafka cluster. The topic to be published to is `chat-messages`.

### Instructions

1. Initialise the environments

    ```bash
    pip install virtualenv
    virtualenv venv
    
    // for mac users
    source venv/bin/activate 

    // for window users
    cd venv/bin/
    activate.bat
    cd ../..

    pip install -r requirements.txt
    ```

2. Insert environment variables

    Insert your own environment variables that is connected to a Kakfa cluster.

    ```bash
    cp .env.example .env
    ```

3. Run the service

    ```bash
    python main.py
    ```
