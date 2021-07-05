from flask import Blueprint, jsonify
from numpy import minimum
from datetime import datetime
import requests
import psycopg2
import warnings
import pandas as pd
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error, mean_absolute_error

warnings.filterwarnings("ignore")

btcData = Blueprint('btc', __name__)

conn = psycopg2.connect(database="postgres", user="postgres",
                        password="Aa@123456", host="127.0.0.1", port="5432")


@btcData.route("/btc/profit/deals", methods=["GET"])
def get_btc_deals():
    res = {}
    cur = conn.cursor()
    cur.execute(
        '''SELECT COUNT(*) FROM Recommendations''')
    rows = cur.fetchall()
    conn.commit()

    res["count"] = rows[0][0]

    result = jsonify(res)
    result.headers.add('Access-Control-Allow-Origin', '*')

    return result


@btcData.route("/btc/recommendation/sell", methods=["GET"])
def post_btc_recommendation_sell():

    ACTUAL_URL = "http://localhost:9000/btc/price"

    actual_res = requests.get(url=ACTUAL_URL)
    actual_data = actual_res.json()[-1:]

    current_time_str = actual_data[0]["datetime"].split(":")

    price = actual_data[0]["price"]

    current_time = datetime.now()
    current_time = current_time.replace(hour=int(current_time_str[0]), minute=int(
        current_time_str[1]), second=int(current_time_str[2]), microsecond=0)

    cur = conn.cursor()
    cur.execute(
        f"INSERT INTO Recommendations (Created_at,recommendation,price) VALUES ('{str(current_time)}', 'SELL', {price})")
    conn.commit()

    res = {}

    res["status"] = "Success"

    result = jsonify(res)
    result.headers.add('Access-Control-Allow-Origin', '*')

    return result


@btcData.route("/btc/recommendation/buy", methods=["GET"])
def post_btc_recommendation_buy():

    ACTUAL_URL = "http://localhost:9000/btc/price"

    actual_res = requests.get(url=ACTUAL_URL)
    actual_data = actual_res.json()[-1:]

    current_time_str = actual_data[0]["datetime"].split(":")

    price = actual_data[0]["price"]

    current_time = datetime.now()
    current_time = current_time.replace(hour=int(current_time_str[0]), minute=int(
        current_time_str[1]), second=int(current_time_str[2]), microsecond=0)

    cur = conn.cursor()
    cur.execute(
        f"INSERT INTO Recommendations (Created_at,recommendation,price) VALUES ('{str(current_time)}', 'BUY', {price})")
    conn.commit()

    res = {}

    res["status"] = "Success"

    result = jsonify(res)
    result.headers.add('Access-Control-Allow-Origin', '*')

    return result


@btcData.route("/btc/profit/details/lastOperation", methods=["GET"])
def get_btc_profit_details_last_operation():
    res = {}
    cur = conn.cursor()
    cur.execute(
        '''SELECT created_at, recommendation, price FROM Recommendations ORDER BY created_at DESC LIMIT 1''')
    rows = cur.fetchall()
    conn.commit()

    if rows[0][1] == "BUY":
        res["price"] = rows[0][2]
    else:
        res["price"] = 0.0

    res["operation"] = rows[0][1]
    res["datetime"] = str(rows[0][0]).split(" ")[1]

    result = jsonify(res)
    result.headers.add('Access-Control-Allow-Origin', '*')

    return result


@btcData.route("/btc/profit/details", methods=["GET"])
def get_btc_profit_details():
    res = []
    cur = conn.cursor()
    cur.execute(
        '''SELECT created_at, recommendation, price FROM Recommendations ORDER BY created_at DESC LIMIT 6''')
    rows = cur.fetchall()
    conn.commit()
    rows.reverse()

    if len(rows) > 2:
        if rows[0][1] == "SELL":
            rows = rows[1:]

    previous_buy = 0

    for i in range(len(rows)):
        current_res = {}

        if str(rows[i][1]) == "BUY":
            previous_buy = rows[i][2]
            current_res["profit/loss"] = 0.0
        else:
            current_res["profit/loss"] = rows[i][2] - previous_buy

        current_res["datetime"] = str(rows[i][0]).split(" ")[1]
        current_res["recommendation"] = str(rows[i][1])
        current_res["price"] = str(rows[i][2])
        res.append(current_res)

    result = jsonify(res)
    result.headers.add('Access-Control-Allow-Origin', '*')

    return result


@btcData.route("/btc/profit", methods=["GET"])
def get_btc_profit():
    res = {}
    cur = conn.cursor()
    cur.execute(
        '''SELECT created_at, recommendation, price FROM Recommendations''')
    rows = cur.fetchall()
    conn.commit()

    if rows[0][1] == "SELL":
        rows = rows[1:]

    if rows[len(rows) - 1][1] == "BUY":
        rows = rows[:-1]

    df = pd.DataFrame(rows, columns=['time', 'recommendation', 'price'])
    df["pct"] = 0
    df["runing_amount"] = 0

    # Investment
    amount = 10000
    transactions_num = len(df)
    transactions_fees = 0.5  # maybe we need to use if statements here
    total_fees = transactions_num * transactions_fees

    for i in range(len(df)):
        if df["recommendation"].iloc[i] == "SELL":
            df["pct"].iloc[i] = (df["price"].iloc[i] -
                                 df["price"].iloc[i-1])/df["price"].iloc[i-1]
            if i <= 1:
                df["runing_amount"].iloc[i] = (1+df["pct"].iloc[i])*amount
            else:
                df["runing_amount"].iloc[i] = (
                    1+df["pct"].iloc[i])*df["runing_amount"].iloc[i-2]

    rtn_pct = (df["runing_amount"].iloc[-1]) / amount * 100

    # dollar profit/loss
    profit_loss = df["runing_amount"].iloc[-1] - amount

    res["rtn_pct"] = rtn_pct
    res["profit_loss"] = profit_loss
    res["runing_amount"] = df["runing_amount"].iloc[-1]

    result = jsonify(res)
    result.headers.add('Access-Control-Allow-Origin', '*')

    return result


@btcData.route("/btc/price", methods=["GET"])
def get_btc_price():
    res = []
    cur = conn.cursor()
    cur.execute('''SELECT avg(price) , to_timestamp(floor((extract('epoch' from Created_at) / 30 )) * 30) AT TIME ZONE 'UTC' new_time 
                    FROM BT_Price
                    WHERE created_at <= date_trunc('hour',  now() + interval '1 hour') and created_at >= (now() - interval '28 minute')
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

#### PREDICTIONS ###


@btcData.route("/predict/ARIMA", methods=["GET"])
def predict_btc_price_arima():
    res = []
    cur = conn.cursor()
    cur.execute('''SELECT to_timestamp(floor((extract('epoch' from Created_at) / 30 )) * 30) AT TIME ZONE 'UTC' time_ , avg(price) price_
                    FROM BTC_Price_Prediction
                    WHERE created_at <= date_trunc('hour',  now() + interval '1 hour') and created_at >= (now() - interval '30 minute')
                    GROUP BY time_ 
                    ORDER BY time_''')
    rows = cur.fetchall()
    for row in rows:
        row_item = {}
        row_item["datetime"] = str(row[0]).split("+")[0].split(" ")[1][:8]
        row_item["price"] = row[1]
        res.append(row_item)
    conn.commit()
    result = jsonify(res)
    result.headers.add('Access-Control-Allow-Origin', '*')

    return result


@btcData.route("/predict/VARMAX", methods=["GET"])
def predict_btc_price_varmax():
    res = []
    cur = conn.cursor()
    cur.execute('''SELECT to_timestamp(floor((extract('epoch' from Created_at) / 30 )) * 30) AT TIME ZONE 'UTC' time_ , avg(price) price_
                    FROM BTC_Price_Prediction_VARMAX
                    WHERE created_at <= date_trunc('hour',  now() + interval '1 hour') and created_at >= (now() - interval '30 minute')
                    GROUP BY time_ 
                    ORDER BY time_''')
    rows = cur.fetchall()
    for row in rows:
        row_item = {}
        row_item["datetime"] = str(row[0]).split("+")[0].split(" ")[1][:8]
        row_item["price"] = row[1]
        res.append(row_item)
    conn.commit()
    result = jsonify(res)
    result.headers.add('Access-Control-Allow-Origin', '*')

    return result


@btcData.route("/predict/SES", methods=["GET"])
def predict_btc_price_ses():
    res = []
    cur = conn.cursor()
    cur.execute('''SELECT to_timestamp(floor((extract('epoch' from Created_at) / 30 )) * 30) AT TIME ZONE 'UTC' time_ , avg(price) price_
                    FROM BTC_Price_Prediction_SES
                    WHERE created_at <= date_trunc('hour',  now() + interval '1 hour') and created_at >= (now() - interval '30 minute')
                    GROUP BY time_ 
                    ORDER BY time_''')
    rows = cur.fetchall()
    for row in rows:
        row_item = {}
        row_item["datetime"] = str(row[0]).split("+")[0].split(" ")[1][:8]
        row_item["price"] = row[1]
        res.append(row_item)
    conn.commit()
    result = jsonify(res)
    result.headers.add('Access-Control-Allow-Origin', '*')

    return result


@btcData.route("/predict/RF", methods=["GET"])
def predict_btc_price_rf():
    res = []
    cur = conn.cursor()
    cur.execute('''SELECT to_timestamp(floor((extract('epoch' from Created_at) / 30 )) * 30) AT TIME ZONE 'UTC' time_ , avg(price) price_
                    FROM BTC_Price_Prediction_RF
                    WHERE created_at <= date_trunc('hour',  now() + interval '1 hour') and created_at >= (now() - interval '30 minute')
                    GROUP BY time_ 
                    ORDER BY time_''')
    rows = cur.fetchall()
    for row in rows:
        row_item = {}
        row_item["datetime"] = str(row[0]).split("+")[0].split(" ")[1][:8]
        row_item["price"] = row[1]
        res.append(row_item)
    conn.commit()
    result = jsonify(res)
    result.headers.add('Access-Control-Allow-Origin', '*')

    return result


@btcData.route("/predict/overall", methods=["GET"])
def predict_btc_price_overall():
    res = []
    cur = conn.cursor()
    cur.execute('''SELECT to_timestamp(floor((extract('epoch' from Created_at) / 30 )) * 30) AT TIME ZONE 'UTC' time_ , avg(price) price_
                    FROM BTC_Price_Prediction_Overall
                    WHERE created_at <= date_trunc('hour',  now() + interval '1 hour') and created_at >= (now() - interval '30 minute')
                    GROUP BY time_ 
                    ORDER BY time_''')
    rows = cur.fetchall()
    for row in rows:
        row_item = {}
        row_item["datetime"] = str(row[0]).split("+")[0].split(" ")[1][:8]
        row_item["price"] = row[1]
        res.append(row_item)
    conn.commit()
    result = jsonify(res)
    result.headers.add('Access-Control-Allow-Origin', '*')

    return result

#### SCORES ###


@btcData.route("/score/ARIMA", methods=["GET"])
def get_model_score_arima():
    res = {}
    cur = conn.cursor()
    cur.execute('''SELECT to_timestamp(floor((extract('epoch' from Created_at) / 30 )) * 30) AT TIME ZONE 'UTC' time_ , avg(price) price_
                    FROM BTC_Price_Prediction
                    WHERE created_at <= date_trunc('hour',  now() + interval '1 hour') and created_at >= (now() - interval '30 minute')
                    GROUP BY time_ 
                    ORDER BY time_''')
    pred_rows = cur.fetchall()

    cur.execute('''SELECT to_timestamp(floor((extract('epoch' from Created_at) / 30 )) * 30) AT TIME ZONE 'UTC' new_time, avg(price)  
                    FROM BT_Price
                    WHERE created_at <= date_trunc('hour',  now() + interval '1 hour') and created_at >= (now() - interval '30 minute')
                    GROUP BY new_time 
                    ORDER BY new_time''')
    actual_rows = cur.fetchall()

    conn.commit()

    actual_df = pd.DataFrame(actual_rows, columns=['time', 'price'])
    preds_df = pd.DataFrame(pred_rows, columns=['time', 'preds'])

    actual_values = [x for x in actual_df["price"]]
    preds_values = [x for x in preds_df["preds"]]

    preds_values = preds_values[:len(actual_values) - 1]
    actual_values = actual_values[:len(preds_values)]

    res["RMSE"] = mean_squared_error(
        actual_values, preds_values, squared=False)
    res["MAE"] = mean_absolute_error(actual_values, preds_values)
    res["MSE"] = mean_squared_error(actual_values, preds_values)

    result = jsonify(res)
    result.headers.add('Access-Control-Allow-Origin', '*')

    return result


@btcData.route("/score/VARMAX", methods=["GET"])
def get_model_score_varmax():
    res = {}
    cur = conn.cursor()
    cur.execute('''SELECT to_timestamp(floor((extract('epoch' from Created_at) / 30 )) * 30) AT TIME ZONE 'UTC' time_ , avg(price) price_
                    FROM BTC_Price_Prediction_VARMAX
                    WHERE created_at <= date_trunc('hour',  now() + interval '1 hour') and created_at >= (now() - interval '30 minute')
                    GROUP BY time_ 
                    ORDER BY time_''')
    pred_rows = cur.fetchall()

    cur.execute('''SELECT to_timestamp(floor((extract('epoch' from Created_at) / 30 )) * 30) AT TIME ZONE 'UTC' new_time, avg(price)  
                    FROM BT_Price
                    WHERE created_at <= date_trunc('hour',  now() + interval '1 hour') and created_at >= (now() - interval '30 minute')
                    GROUP BY new_time 
                    ORDER BY new_time''')
    actual_rows = cur.fetchall()

    conn.commit()

    actual_df = pd.DataFrame(actual_rows, columns=['time', 'price'])
    preds_df = pd.DataFrame(pred_rows, columns=['time', 'preds'])

    actual_values = [x for x in actual_df["price"]]
    preds_values = [x for x in preds_df["preds"]]

    preds_values = preds_values[:len(actual_values) - 1]
    actual_values = actual_values[:len(preds_values)]

    res["RMSE"] = mean_squared_error(
        actual_values, preds_values, squared=False)
    res["MAE"] = mean_absolute_error(actual_values, preds_values)
    res["MSE"] = mean_squared_error(actual_values, preds_values)

    result = jsonify(res)
    result.headers.add('Access-Control-Allow-Origin', '*')

    return result


@btcData.route("/score/SES", methods=["GET"])
def get_model_score_ses():
    res = {}
    cur = conn.cursor()
    cur.execute('''SELECT to_timestamp(floor((extract('epoch' from Created_at) / 30 )) * 30) AT TIME ZONE 'UTC' time_ , avg(price) price_
                    FROM BTC_Price_Prediction
                    WHERE created_at <= date_trunc('hour',  now() + interval '1 hour') and created_at >= (now() - interval '30 minute')
                    GROUP BY time_ 
                    ORDER BY time_''')
    pred_rows = cur.fetchall()

    cur.execute('''SELECT to_timestamp(floor((extract('epoch' from Created_at) / 30 )) * 30) AT TIME ZONE 'UTC' new_time, avg(price)  
                    FROM BTC_Price_Prediction_SES
                    WHERE created_at <= date_trunc('hour',  now() + interval '1 hour') and created_at >= (now() - interval '30 minute')
                    GROUP BY new_time 
                    ORDER BY new_time''')
    actual_rows = cur.fetchall()

    conn.commit()

    actual_df = pd.DataFrame(actual_rows, columns=['time', 'price'])
    preds_df = pd.DataFrame(pred_rows, columns=['time', 'preds'])

    actual_values = [x for x in actual_df["price"]]
    preds_values = [x for x in preds_df["preds"]]

    preds_values = preds_values[:len(actual_values) - 1]
    actual_values = actual_values[:len(preds_values)]

    res["RMSE"] = mean_squared_error(
        actual_values, preds_values, squared=False)
    res["MAE"] = mean_absolute_error(actual_values, preds_values)
    res["MSE"] = mean_squared_error(actual_values, preds_values)

    result = jsonify(res)
    result.headers.add('Access-Control-Allow-Origin', '*')

    return result


@btcData.route("/score/RF", methods=["GET"])
def get_model_score_RF():
    res = {}
    cur = conn.cursor()
    cur.execute('''SELECT to_timestamp(floor((extract('epoch' from Created_at) / 30 )) * 30) AT TIME ZONE 'UTC' time_ , avg(price) price_
                    FROM BTC_Price_Prediction
                    WHERE created_at <= date_trunc('hour',  now() + interval '1 hour') and created_at >= (now() - interval '30 minute')
                    GROUP BY time_ 
                    ORDER BY time_''')
    pred_rows = cur.fetchall()

    cur.execute('''SELECT to_timestamp(floor((extract('epoch' from Created_at) / 30 )) * 30) AT TIME ZONE 'UTC' new_time, avg(price)  
                    FROM BTC_Price_Prediction_RF
                    WHERE created_at <= date_trunc('hour',  now() + interval '1 hour') and created_at >= (now() - interval '30 minute')
                    GROUP BY new_time 
                    ORDER BY new_time''')
    actual_rows = cur.fetchall()

    conn.commit()

    actual_df = pd.DataFrame(actual_rows, columns=['time', 'price'])
    preds_df = pd.DataFrame(pred_rows, columns=['time', 'preds'])

    actual_values = [x for x in actual_df["price"]]
    preds_values = [x for x in preds_df["preds"]]

    min_val = minimum(len(actual_values), len(preds_values))

    preds_values = preds_values[:min_val-1]
    actual_values = actual_values[:min_val-1]

    res["RMSE"] = mean_squared_error(
        actual_values, preds_values, squared=False)
    res["MAE"] = mean_absolute_error(actual_values, preds_values)
    res["MSE"] = mean_squared_error(actual_values, preds_values)

    result = jsonify(res)
    result.headers.add('Access-Control-Allow-Origin', '*')

    return result


@btcData.route("/score/overall", methods=["GET"])
def get_model_score_overall():
    cur = conn.cursor()
    cur.execute('''SELECT to_timestamp(floor((extract('epoch' from Created_at) / 30 )) * 30) AT TIME ZONE 'UTC' time_ , avg(price) price_
                    FROM BT_Price
                    WHERE created_at <= date_trunc('hour',  now() + interval '1 hour') and created_at >= (now() - interval '1 hour')
                    GROUP BY time_ 
                    ORDER BY time_''')
    actual_rows = cur.fetchall()

    cur.execute('''SELECT to_timestamp(floor((extract('epoch' from Created_at) / 30 )) * 30) AT TIME ZONE 'UTC' time_ , avg(price) price_
                    FROM BTC_Price_Prediction_Overall
                    WHERE created_at <= date_trunc('hour',  now() + interval '1 hour') and created_at >= (now() - interval '1 hour')
                    GROUP BY time_ 
                    ORDER BY time_''')
    preds_rows = cur.fetchall()
    conn.commit()

    actual_df = pd.DataFrame(actual_rows, columns=['time', 'price'])
    preds_df = pd.DataFrame(preds_rows, columns=['time', 'preds'])

    actual_values = [x for x in actual_df["price"]]
    preds_values = [x for x in preds_df["preds"]]

    min_val = minimum(len(actual_values), len(preds_values))

    preds_values = preds_values[:min_val-1]
    actual_values = actual_values[:min_val-1]

    r2 = r2_score(actual_values, preds_values)

    res = {}

    res["R2"] = r2

    result = jsonify(res)
    result.headers.add('Access-Control-Allow-Origin', '*')

    return result
