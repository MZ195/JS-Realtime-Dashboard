import requests
from datetime import datetime
import psycopg2
import time

conn = psycopg2.connect(database="postgres", user="postgres",
                        password="Aa@123456", host="127.0.0.1", port="5432")

PREDS_URL = "http://localhost:9000/predict/overall"
ACTUAL_URL = "http://localhost:9000/btc/price"
SCORE_URL = "http://localhost:9000/score/overall"

previous_action = ""
previous_buy = 0
previous_sell = 0

while(1):
    actual_res = requests.get(url=ACTUAL_URL)
    actual_data = actual_res.json()[-2:]

    PREDS_res = requests.get(url=PREDS_URL)
    PREDS_data = PREDS_res.json()[-4:]

    SCORE_res = requests.get(url=SCORE_URL)
    SCORE_data = SCORE_res.json()

    cur = conn.cursor()
    cur.execute(
        '''SELECT created_at, recommendation, price FROM Recommendations ORDER BY created_at DESC LIMIT 2''')
    rows = cur.fetchall()
    conn.commit()

    rows.reverse()

    if len(rows) > 1 and rows[1][1] == "SELL":
        previous_buy = rows[0][2]
        previous_sell = rows[1][2]
        previous_action = rows[1][1]
    elif rows[1][1] == "BUY":
        previous_buy = rows[1][2]
        previous_sell = rows[0][2]
        previous_action = rows[1][1]

    cur = conn.cursor()
    cur.execute(
        '''SELECT AVG(price), stddev(price) FROM BT_Price WHERE created_at <= date_trunc('hour',  now() + interval '1 hour') and created_at >= (now() - interval '1 hour')''')
    rows = cur.fetchall()
    conn.commit()

    price_avg = rows[0][0]
    price_std = rows[0][1]

    pos_range = price_avg + price_std
    neg_range = price_avg - price_std

    avg1 = (PREDS_data[0]["price"] + PREDS_data[1]["price"])/2

    diff1 = (avg1 - actual_data[0]["price"])
    pred_signal1 = ""
    if diff1 < 0:
        pred_signal1 = "Resistance_Breakout"
    else:
        pred_signal1 = "Support_Breakout"

    avg2 = (PREDS_data[2]["price"] + PREDS_data[3]["price"])/2

    diff2 = (avg2 - actual_data[1]["price"])

    pred_signal2 = ""
    if diff2 < 0:
        pred_signal2 = "Resistance_Breakout"
    else:
        pred_signal2 = "Support_Breakout"

    current_time_str = actual_data[1]["datetime"].split(":")

    price = actual_data[1]["price"]

    current_time = datetime.now()
    current_time = current_time.replace(
        hour=int(current_time_str[0]), minute=int(current_time_str[1]), second=int(current_time_str[2]), microsecond=0)

    if (pred_signal2 == "Support_Breakout" and
        pred_signal1 == "Resistance_Breakout" and
        SCORE_data["R2"] > 0.85 and
        previous_action != "SELL" and
            price >= (previous_buy + (price_std*2))):
        recom = "SELL"
        cur = conn.cursor()
        cur.execute(
            f"INSERT INTO Recommendations (Created_at,recommendation,price) VALUES ('{str(current_time)}', '{recom}', {price})")
        conn.commit()

    if (pred_signal2 == "Resistance_Breakout" and
        pred_signal1 == "Support_Breakout" and
        SCORE_data["R2"] > 0.85 and
            previous_action != "BUY"):
        if price >= neg_range and price <= pos_range:
            recom = "BUY"
            cur = conn.cursor()
            cur.execute(
                f"INSERT INTO Recommendations (Created_at,recommendation,price) VALUES ('{str(current_time)}', '{recom}', {price})")
            conn.commit()

    time.sleep(15)
