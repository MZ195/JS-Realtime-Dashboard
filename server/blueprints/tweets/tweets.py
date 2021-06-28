from flask import Blueprint, jsonify
import psycopg2
import warnings
from datetime import datetime

warnings.filterwarnings("ignore")

tweetsData = Blueprint('tweets', __name__)

conn = psycopg2.connect(database="postgres", user="postgres",
                        password="Aa@123456", host="127.0.0.1", port="5432")


@tweetsData.route("/tweets/pos", methods=["GET"])
def get_positive_tweets():
    res = []
    cur = conn.cursor()
    cur.execute('''SELECT sum(Positive) , 
    to_timestamp(floor((extract('epoch' from Created_at AT TIME ZONE 'UTC') / 30 )) * 30)  new_time 
    FROM tweets 
 	WHERE Created_at <= date_trunc('hour',  now() + interval '1 hour') AT TIME ZONE 'UTC' and Created_at > (now() - interval '30 minute') AT TIME ZONE 'UTC'
    GROUP BY new_time 
    ORDER BY new_time''')
    rows = cur.fetchall()
    for row in rows:
        row_item = {}
        row_item["datetime"] = str(row[1]).split("+")[0].split(" ")[1][:8]
        row_item["count"] = row[0]
        res.append(row_item)
    conn.commit()
    result = jsonify(res)
    result.headers.add('Access-Control-Allow-Origin', '*')

    return result


@tweetsData.route("/tweets/neg", methods=["GET"])
def get_negative_tweets():
    res = []
    cur = conn.cursor()
    cur.execute('''SELECT sum(Negative) , 
    to_timestamp(floor((extract('epoch' from Created_at AT TIME ZONE 'UTC') / 30 )) * 30)  new_time 
    FROM tweets 
 	WHERE Created_at <= date_trunc('hour',  now() + interval '1 hour') AT TIME ZONE 'UTC' and Created_at > (now() - interval '30 minute') AT TIME ZONE 'UTC'
    GROUP BY new_time 
    ORDER BY new_time''')
    rows = cur.fetchall()
    for row in rows:
        row_item = {}
        row_item["datetime"] = str(row[1]).split("+")[0][:8]
        row_item["count"] = row[0]
        res.append(row_item)
    conn.commit()
    result = jsonify(res)
    result.headers.add('Access-Control-Allow-Origin', '*')

    return result


@tweetsData.route("/tweets/count", methods=["GET"])
def get_count_tweets():
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


@tweetsData.route("/tweets/daily", methods=["GET"])
def get_daily_tweets():
    res = []
    cur = conn.cursor()
    cur.execute('''SELECT sum(Negative), sum(Positive) , 
                    extract(hour from created_at AT TIME ZONE 'UTC') new_time
                    FROM tweets 
                    WHERE created_at <= date_trunc('day',  now() + interval '1 day') AT TIME ZONE 'UTC' and created_at >= date_trunc('day',  now()) AT TIME ZONE 'UTC'
                    GROUP BY new_time 
                    ORDER BY new_time''')
    rows = cur.fetchall()
    for row in rows:
        current_time = datetime.now()
        newdatetime = current_time.replace(hour=int(row[2]), minute=0)
        row_item = {}
        row_item["datetime"] = str(newdatetime).split(" ")[1].split(".")[0][:5]
        row_item["neg"] = row[0]
        row_item["pos"] = row[1]
        res.append(row_item)
    conn.commit()
    result = jsonify(res)
    result.headers.add('Access-Control-Allow-Origin', '*')

    return result
