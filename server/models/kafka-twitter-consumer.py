from nltk.sentiment import SentimentIntensityAnalyzer
from kafka import KafkaProducer, KafkaConsumer
from kafka import KafkaConsumer
from json import loads, dumps
from datetime import datetime
import psycopg2


def setup():
    # Create Database connection
    conn = psycopg2.connect(database="postgres", user="postgres",
                            password="Aa@123456", host="127.0.0.1", port="5432")

    # Initilize the sentiment analyzer
    sia = SentimentIntensityAnalyzer()

    return conn, sia


def consume_data():
    # setup the database connection & Sentiment Analyzer
    conn, sia = setup()

    # Create Kafka consumer
    consumer = KafkaConsumer('important_tweets', bootstrap_servers=['127.0.0.1:9092'], auto_offset_reset='earliest',
                             enable_auto_commit=True, group_id='twitter-analyzer', value_deserializer=lambda x: loads(x.decode('utf-8')))

    for message in consumer:
        message = message.value
        producer_results(conn, sia, message)


def producer_results(conn, sia, msg):
    # perform Sentiment analysis
    pred = sia.polarity_scores(msg["text"])

    # format the date object
    date_time_str = msg["created_at"]
    test = date_time_str.split(" ")
    test2 = test[2] + " " + test[1] + " " + test[5] + " " + test[3]
    date_time_obj = datetime.strptime(test2, '%d %b %Y %H:%M:%S')

    # Get user location
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

    pos, neg, neu = 0, 0, 0
    if pred["compound"] == 0:
        neu = 1
    elif pred["compound"] > 0:
        pos = 1
    else:
        neg = 1

    cur = conn.cursor()
    cur.execute(
        f"INSERT INTO tweets (Created_at,Positive,Negative,Neutral) VALUES ('{date_time_obj}', {pos}, {neg}, {neu})")
    conn.commit()


if __name__ == "__main__":
    consume_data()
