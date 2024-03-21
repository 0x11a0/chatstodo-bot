# ChatsTodo Bots

### Setup instructions

1. Run Docker application locally

1. Start Docker compose and build

   ```
   docker compose up -d --build
   ```

1. View logs

   ```
   docker compose logs
   ```

1. Stop Docker

   ```
   docker compose down
   ```

### Ports

- 8001: Telegram
- 8002: Discord

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
