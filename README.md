# ChatsTodo Bots

### Format of String package to send to Kafka

This is the format to follow when sending messages to Kafka.

```json
{
  "platform": "",
  "sender_user_id": "",
  "group_id": "", // an ID
  "timestamp": "", // in ISO
  "message": ""
}
```

### Instructions to start

1. Run docker locally

1. Set up env file

   ```
   cp .env.example .env
   ```

1. Start and build docker compose

   ```
   docker compose up -d --build
   ```

1. View logs

   ```
   docker compose logs
   ```

1. Stop docker compose

   ```
   docker compose down
   ```
