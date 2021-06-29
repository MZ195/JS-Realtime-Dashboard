from flask import Blueprint, jsonify
import psycopg2
import warnings
import pandas as pd
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error, mean_absolute_error

warnings.filterwarnings("ignore")

btcData = Blueprint('btc', __name__)

conn = psycopg2.connect(database="postgres", user="postgres",
                        password="Aa@123456", host="127.0.0.1", port="5432")


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

    preds = []
    actual = []

    for i in range(len(actual_rows)):
        preds.append(pred_rows[i][1])
        actual.append(actual_rows[i][1])

    res["RMSE"] = mean_squared_error(actual, preds, squared=False)
    res["MAE"] = mean_absolute_error(actual, preds)
    res["MSE"] = mean_squared_error(actual, preds)

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

    preds = []
    actual = []

    for i in range(len(actual_rows)):
        preds.append(pred_rows[i][1])
        actual.append(actual_rows[i][1])

    res["RMSE"] = mean_squared_error(actual, preds, squared=False)
    res["MAE"] = mean_absolute_error(actual, preds)
    res["MSE"] = mean_squared_error(actual, preds)

    result = jsonify(res)
    result.headers.add('Access-Control-Allow-Origin', '*')

    return result


@btcData.route("/score/overall", methods=["GET"])
def get_model_score_overall():
    cur = conn.cursor()
    cur.execute('''SELECT to_timestamp(floor((extract('epoch' from Created_at) / 30 )) * 30) AT TIME ZONE 'UTC' time_ , avg(price) price_
                    FROM BT_Price
                    WHERE created_at <= date_trunc('hour',  now() + interval '1 hour') and created_at >= (now() - interval '30 minute')
                    GROUP BY time_ 
                    ORDER BY time_''')
    actual_rows = cur.fetchall()

    cur.execute('''SELECT to_timestamp(floor((extract('epoch' from Created_at) / 30 )) * 30) AT TIME ZONE 'UTC' time_ , avg(price) price_
                    FROM BTC_Price_Prediction_Overall
                    WHERE created_at <= date_trunc('hour',  now() + interval '1 hour') and created_at >= (now() - interval '30 minute')
                    GROUP BY time_ 
                    ORDER BY time_''')
    preds_rows = cur.fetchall()
    conn.commit()

    actual_df = pd.DataFrame(actual_rows, columns=['time', 'price'])
    preds_df = pd.DataFrame(preds_rows, columns=['time', 'preds'])

    actual_values = [x for x in actual_df["price"]]
    preds_values = [x for x in preds_df["preds"]]

    preds_values = preds_values[:len(actual_values) - 1]
    actual_values = actual_values[:len(preds_values)]

    r2 = r2_score(actual_values, preds_values)

    res = {}

    res["R2"] = r2

    result = jsonify(res)
    result.headers.add('Access-Control-Allow-Origin', '*')

    return result
