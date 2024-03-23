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

### Formats

#### String package to send to Kafka

This is the format to follow when sending messages to Kafka.

```json
{
  "platform": "",
  "sender_name": "",
  "group_id": "", // an ID
  "timestamp": "", // in ISO
  "message": ""
}
```

#### Group data to send to mongodb

Send to collections, `Groups`

```json
{
  "user_id": "", // str
  "group_id": "", // str
  "group_name": "",
  "platform": "",
  "created_at": "" // in ISO URC
}
```
