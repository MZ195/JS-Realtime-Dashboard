import pandas as pd
import warnings
from datetime import datetime, timedelta
from statsmodels.tsa.statespace.varmax import VARMAX
import psycopg2
import time

warnings.filterwarnings("ignore")

conn = psycopg2.connect(database="postgres", user="postgres",
                        password="Aa@123456", host="127.0.0.1", port="5432")

while(1):

    cur = conn.cursor()
    cur.execute('''SELECT to_timestamp(floor((extract('epoch' from Created_at) / 30 )) * 30) AT TIME ZONE 'UTC' time_ , avg(price) price_
                                FROM BT_Price
                                WHERE created_at <= date_trunc('hour',  now() + interval '1 hour') and created_at >= (now() - interval '1 hour')
                                GROUP BY time_
                                ORDER BY time_''')
    btc_rows = cur.fetchall()
    conn.commit()

    cur = conn.cursor()
    cur.execute('''SELECT to_timestamp(floor((extract('epoch' from Created_at) / 30 )) * 30) time_ , COUNT(*)
                            FROM tweets
                            WHERE created_at <= date_trunc('hour',  now() + interval '1 hour') AT TIME ZONE 'UTC' and created_at >= (now() - interval '1 hour') AT TIME ZONE 'UTC'
                            GROUP BY time_
                            ORDER BY time_''')
    tweets_rows = cur.fetchall()
    conn.commit()

    btc_df = pd.DataFrame(btc_rows, columns=['time', 'price'])
    tweets_df = pd.DataFrame(tweets_rows, columns=['time', 'count'])
    btc_df.time = btc_df["time"].astype(str)
    tweets_df.time = tweets_df["time"].astype(str)
    tweets_df.time = tweets_df["time"].map(lambda x: x.split("+")[0])
    merge_df = pd.merge(btc_df, tweets_df, on='time')
    merge_df = merge_df.drop(["time"], axis=1)

    history = [list(x) for x in merge_df.values]

    results = []
    try:
        for i in range(0, 2):
            current_time = datetime.now() + timedelta(seconds=(i * 30))
            model = VARMAX(history, order=(1, 1))
            model_fit = model.fit(disp=False)
            output = model_fit.forecast()
            yhat = output[0]

            if current_time.second < 30:
                newdatetime = current_time.replace(second=30, microsecond=0)
            elif current_time.minute + 1 <= 59:
                newdatetime = current_time.replace(
                    minute=(current_time.minute + (1)), second=0, microsecond=0)
            elif (current_time.minute == 59 and current_time.hour != 23):
                newdatetime = current_time.replace(
                    hour=(current_time.hour + 1), minute=0, second=0, microsecond=0)
            elif(current_time.minute == 59 and current_time.hour == 23):
                newdatetime = current_time.replace(
                    day=(current_time.day + 1), hour=0, minute=0, second=0, microsecond=0)
            else:
                newdatetime = current_time.replace(
                    hour=(current_time.hour + 1), minute=0, second=0, microsecond=0)

            if yhat[0] < 0:
                yhat[0] = merge_df["price"].mean()
            history.append(yhat)
            cur = conn.cursor()
            cur.execute(
                f"INSERT INTO BTC_Price_Prediction_VARMAX (created_at,price) VALUES ('{str(newdatetime)}', {yhat[0]})")
            conn.commit()
    except:
        continue
    time.sleep(15)
