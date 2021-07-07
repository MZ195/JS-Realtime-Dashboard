from nltk.sentiment import SentimentIntensityAnalyzer
from kafka import KafkaProducer, KafkaConsumer
from kafka import KafkaConsumer
from json import loads, dumps
from datetime import datetime
import psycopg2

# Create Database connection
conn = psycopg2.connect(database="postgres", user="postgres",
                        password="Aa@123456", host="127.0.0.1", port="5432")

# Initilize the sentiment analyzer
sia = SentimentIntensityAnalyzer()


def consume_data():

    # Create Kafka consumer
    consumer = KafkaConsumer('important_tweets', bootstrap_servers=['127.0.0.1:9092'], auto_offset_reset='earliest',
                             enable_auto_commit=True, group_id='twitter-analyzer', value_deserializer=lambda x: loads(x.decode('utf-8')))
    
    # Create Kafka producer
    producer = KafkaProducer(bootstrap_servers=[
        '127.0.0.1:9092'], value_serializer=lambda x: dumps(x).encode('utf-8'))
    for message in consumer:
        message = message.value
        producer_results(message, producer)


def producer_results(msg, producer):
    pred = sia.polarity_scores(msg["text"])
    date_time_str = msg["created_at"]
    test = date_time_str.split(" ")
    test2 = test[2] + " " + test[1] + " " + test[5] + " " + test[3]
    date_time_obj = datetime.strptime(test2, '%d %b %Y %H:%M:%S')

    if msg["user"]["location"] != None:
        if "," in msg["user"]["location"] and "'" not in msg["user"]["location"]:
            location_ = msg["user"]["location"]
            geo = None
            coordinates = None
            place = None
            cur = conn.cursor()
            cur.execute(
                f"INSERT INTO Tweets_location (Created_at,location_,geo,coordinates,place) VALUES ('{date_time_obj}', '{location_}', '{geo}', '{coordinates}', '{place}')")
            conn.commit()

    res = {}
    res["created_at"] = str(date_time_obj)
    res["tweet"] = msg["text"]
    res["neg"] = pred["neg"]
    res["neu"] = pred["neu"]
    res["pos"] = pred["pos"]
    res["compound"] = pred["compound"]
    producer.send('analyzed_tweets', value=res)

    pos, neg, neu = 0, 0, 0

    if pred["compound"] == 0:
        neu = 1
    elif pred["compound"] > 0:
        pos = 1
    else:
        neg = 1

    tweet_text = msg["text"]
    cur = conn.cursor()
    cur.execute(
        f"INSERT INTO tweets (Created_at,Positive,Negative,Neutral) VALUES ('{date_time_obj}', {pos}, {neg}, {neu})")
    conn.commit()


if __name__ == "__main__":
    consume_data()
