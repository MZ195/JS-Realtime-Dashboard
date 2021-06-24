from flask import Blueprint, jsonify
import psycopg2

sentimentData = Blueprint('sentimentData', __name__)

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
        row_item["datetime"] = str(row[1]).split("+")[0].split(" ")[1][:8]
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
        row_item["datetime"] = str(row[1]).split("+")[0][:8]
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


@sentimentData.route("/get_price/", methods=["GET"])
def index4():
    res = []
    cur = conn.cursor()
    cur.execute('''SELECT avg(price) , to_timestamp(floor((extract('epoch' from Created_at) / 30 )) * 30) AT TIME ZONE 'UTC' new_time 
                    FROM BT_Price
                    where created_at <= date_trunc('hour',  now() + interval '1 hour') and created_at >= date_trunc('hour',  now())
                    GROUP BY new_time 
                    ORDER BY new_time''')
    rows = cur.fetchall()
    for row in rows:
        row_item = {}
        row_item["datetime"] = str(row[1]).split("+")[0].split(" ")[1][:8]
        row_item["price"] = row[0]
        res.append(row_item)
    conn.commit()
    result = jsonify(res)
    result.headers.add('Access-Control-Allow-Origin', '*')

    return result
    # res = {}

    # URL = "https://api.coindesk.com/v1/bpi/currentprice.json"
    # r = requests.get(url=URL)

    # current_time = datetime.datetime.now()
    # res["datetime"] = str(current_time).split(" ")[1].split(".")[0][:8]

    # data = r.json()
    # res["price"] = data["bpi"]["USD"]["rate_float"]

    # result = jsonify(res)
    # result.headers.add('Access-Control-Allow-Origin', '*')

    # return result
