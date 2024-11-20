# Real-Time YouTube Analytics Streamed to Telegram

This Python-based project aims to fetch real-time YouTube metrics like likes, views, comments, and favorites, and then streams this data via Kafka. 
Also, KSqlDB was used for stream processing and the processed data is then sent to a Telegram bot for real-time notifications.

## Tech Stack

- Python
- Docker
- Kafka
- Confluent Containers (Zookeeper, Kafka, Schema Registry, Connect, ksqlDB, Control Center)
- Telegram API

## System Architecture
![image](https://github.com/user-attachments/assets/0b51aa2f-f32c-4bf5-b654-a5c1cafbce74)

## How it works
1. Fetch streaming data from YouTube API using the given playlist ID.

2. Send videos' metrics to Kafka and create topics.

   *Here we are trying to fectch video metrics (views, likes, comments) from the "NBA 2024-2025: Best Duel" playlist:*
   ![image](https://github.com/user-attachments/assets/a19f2c01-474d-443a-87aa-385c31dfb6f5)
   
3. Performs real-time analytics using ksqlDB.

   *For instnace, we want to calculate the difference from the last two update on likes so that we can know which video is trending:*
   ![image](https://github.com/user-attachments/assets/0bd37f24-25e6-4cf8-9768-779164ac4017)

   **Check out the [video demo](https://drive.google.com/file/d/1YpDXfZD3p88gRqrEYnbs0DefzHgE4JFP/view?usp=drive_link) here.**

   
5. The analytics results are then sent to Telegram for real-time notifications.

   ![image](https://github.com/user-attachments/assets/9e430ca8-e3e4-4cc3-a88b-d2dcbb8404c8)





   
