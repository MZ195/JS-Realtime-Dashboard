from flask import Blueprint, jsonify
import psycopg2
from statsmodels.tsa.statespace.varmax import VARMAX
import warnings
from datetime import datetime

from sklearn.metrics import mean_squared_error, mean_absolute_error

warnings.filterwarnings("ignore")

sentimentData = Blueprint('sentimentData', __name__)

conn = psycopg2.connect(database="postgres", user="postgres",
                        password="Aa@123456", host="127.0.0.1", port="5432")


@sentimentData.route("/pos/", methods=["GET"])
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


@sentimentData.route("/neg/", methods=["GET"])
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


@sentimentData.route("/pos_count/", methods=["GET"])
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


@sentimentData.route("/daily_tweets/", methods=["GET"])
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


@sentimentData.route("/daily_summary/", methods=["GET"])
def get_daily_summary():
    res = []
    cur = conn.cursor()
    cur.execute('''SELECT sum(Negative), sum(Positive) , 
                        extract(hour from created_at AT TIME ZONE 'UTC') new_time
                        FROM tweets 
                        WHERE created_at <= date_trunc('day',  now() + interval '1 day') AT TIME ZONE 'UTC' and created_at >= date_trunc('day',  now()) AT TIME ZONE 'UTC'
                        GROUP BY new_time 
                        ORDER BY new_time''')
    res_1_rows = cur.fetchall()
    conn.commit()

    cur.execute('''SELECT avg(price) , 
                        extract(hour from created_at) new_time
                        FROM BT_Price
                        WHERE created_at <= date_trunc('day',  now() + interval '1 day') and created_at >= date_trunc('day',  now())
                        GROUP BY new_time 
                        ORDER BY new_time''')
    res_2_rows = cur.fetchall()
    conn.commit()

    tweets_time = []
    prices_time = []
    for row in res_1_rows:
        tweets_time.append(row[2])
    for row in res_2_rows:
        prices_time.append(row[1])

    for i in range(len(tweets_time)):
        if(tweets_time[i] != prices_time[i]):
            prices_time.insert(i, tweets_time[i])
            res_2_rows.insert(i, (0.0, tweets_time[i]))

    for i in range(len(res_1_rows)):
        current_tweet_row = res_1_rows[i]
        current_price_row = res_2_rows[i]
        current_time = datetime.now()
        newdatetime = current_time.replace(
            hour=int(current_tweet_row[2]), minute=0)
        row_item = {}
        row_item["datetime"] = str(newdatetime).split(" ")[1].split(".")[0][:5]
        row_item["neg"] = current_tweet_row[0]
        row_item["pos"] = current_tweet_row[1]
        row_item["price"] = current_price_row[0]
        res.append(row_item)

    result = jsonify(res)
    result.headers.add('Access-Control-Allow-Origin', '*')

    return result


@sentimentData.route("/get_price/", methods=["GET"])
def get_btc_price():
    res = []
    cur = conn.cursor()
    cur.execute('''SELECT avg(price) , to_timestamp(floor((extract('epoch' from Created_at) / 30 )) * 30) AT TIME ZONE 'UTC' new_time 
                    FROM BT_Price
                    WHERE created_at <= date_trunc('hour',  now() + interval '1 hour') and created_at >= (now() - interval '29 minute')
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


@sentimentData.route("/predict_VARMAX/", methods=["GET"])
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


@sentimentData.route("/predict_ARIMA/", methods=["GET"])
def predict_btc_price_arima():
    res = []
    cur = conn.cursor()
    cur.execute('''SELECT to_timestamp(floor((extract('epoch' from Created_at) / 30 )) * 30) AT TIME ZONE 'UTC' time_ , avg(price) price_
                    FROM BTC_Price_Prediction
                    WHERE created_at <= date_trunc('hour',  now() + interval '1 hour') and created_at >= (now() - interval '29 minute')
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


@sentimentData.route("/predict_SES/", methods=["GET"])
def predict_btc_price_ses():
    res = []
    cur = conn.cursor()
    cur.execute('''SELECT to_timestamp(floor((extract('epoch' from Created_at) / 30 )) * 30) AT TIME ZONE 'UTC' time_ , avg(price) price_
                    FROM BTC_Price_Prediction_SES
                    WHERE created_at <= date_trunc('hour',  now() + interval '1 hour') and created_at >= (now() - interval '29 minute')
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


@sentimentData.route("/score_VARMAX/", methods=["GET"])
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
                    WHERE created_at <= date_trunc('hour',  now() + interval '1 hour') and created_at >= (now() - interval '29 minute')
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


@sentimentData.route("/score_ARIMA/", methods=["GET"])
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
                    WHERE created_at <= date_trunc('hour',  now() + interval '1 hour') and created_at >= (now() - interval '29 minute')
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


@sentimentData.route("/score_SES/", methods=["GET"])
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
                    WHERE created_at <= date_trunc('hour',  now() + interval '1 hour') and created_at >= (now() - interval '29 minute')
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
