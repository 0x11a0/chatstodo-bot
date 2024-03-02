# ChatsTodo Bots

### Format of String package to send to Kafka

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