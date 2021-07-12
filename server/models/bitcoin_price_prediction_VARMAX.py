import pandas as pd
from datetime import datetime, timedelta
from statsmodels.tsa.statespace.varmax import VARMAX
import time
import SQL_STATEMENTS


def date_formating(current_time):
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
    return newdatetime


def predict_VARMAX():
    conn = SQL_STATEMENTS.setup()

    while(1):
        cur = conn.cursor()
        cur.execute(SQL_STATEMENTS.BTC_PRICE_1_HOUR_WINDOW)
        btc_rows = cur.fetchall()
        conn.commit()

        cur = conn.cursor()
        cur.execute(SQL_STATEMENTS.TWEETS_1_HOUR_WINDOW)
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

        # (BTC Price, Count of tweets)
        try:
            for i in range(0, 2):
                current_time = datetime.now() + timedelta(seconds=(i * 30))
                model = VARMAX(history, order=(1, 1))
                model_fit = model.fit(disp=False)
                output = model_fit.forecast()
                yhat = output[0]
                newdatetime = date_formating(current_time)
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
