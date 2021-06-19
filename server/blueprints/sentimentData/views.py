from flask import Blueprint, jsonify
from nltk.sentiment import SentimentIntensityAnalyzer
import psycopg2
from json import dumps
from kafka import KafkaProducer

sia = SentimentIntensityAnalyzer()

sentimentData = Blueprint('sentimentData', __name__)
producer = KafkaProducer(bootstrap_servers=[
                         '127.0.0.1:9092'], value_serializer=lambda x: dumps(x).encode('utf-8'))

conn = psycopg2.connect(database="postgres", user="postgres",
                        password="Aa@123456", host="127.0.0.1", port="5432")


@sentimentData.route("/pos/", methods=["GET"])
def index():
    res = []
    cur = conn.cursor()
    cur.execute('''SELECT sum(Positive) , 
    to_timestamp(floor((extract('epoch' from Created_at) / 60 )) * 60) new_time
    FROM tweets GROUP BY new_time ORDER BY new_time''')
    rows = cur.fetchall()
    for row in rows:
        row_item = {}
        row_item["datetime"] = str(row[1]).split("+")[0].split(" ")[1]
        row_item["count"] = row[0]
        res.append(row_item)
    conn.commit()
    result = jsonify(res)
    result.headers.add('Access-Control-Allow-Origin', '*')

    return result


@sentimentData.route("/neg/", methods=["GET"])
def index2():
    res = []
    cur = conn.cursor()
    cur.execute('''SELECT sum(Negative) , 
    to_timestamp(floor((extract('epoch' from Created_at) / 60 )) * 60) new_time
    FROM tweets GROUP BY new_time ORDER BY new_time''')
    rows = cur.fetchall()
    for row in rows:
        row_item = {}
        row_item["datetime"] = str(row[1]).split("+")[0].split(" ")[1]
        row_item["count"] = row[0]
        res.append(row_item)
    conn.commit()
    result = jsonify(res)
    result.headers.add('Access-Control-Allow-Origin', '*')

    return result


@sentimentData.route("/pos_count/", methods=["GET"])
def index3():
    res = {}
    cur = conn.cursor()
    cur.execute(
        '''SELECT sum(Positive) pos_sum, sum(Negative) neg_sum FROM tweets''')
    rows = cur.fetchall()
    res["Total_pos"] = rows[0][0]
    res["Total_neg"] = rows[0][1]
    conn.commit()
    result = jsonify(res)
    result.headers.add('Access-Control-Allow-Origin', '*')

    return result
