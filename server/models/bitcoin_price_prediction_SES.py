import pandas as pd
import warnings
from datetime import datetime, timedelta
from statsmodels.tsa.holtwinters import SimpleExpSmoothing
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
    rows = cur.fetchall()
    conn.commit()

    df = pd.DataFrame(rows, columns=['time', 'price'])
    history = [x for x in df["price"].values]

    results = []
    for i in range(0, 2):
        current_time = datetime.now() + timedelta(seconds=(i * 30))
        model = SimpleExpSmoothing(history)
        model_fit = model.fit()
        output = model_fit.forecast()
        yhat = output[0]
        try:
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
        except:
            continue

        history.append(yhat)
        cur = conn.cursor()
        cur.execute(
            f"INSERT INTO BTC_Price_Prediction_SES (created_at,price) VALUES ('{str(newdatetime)}', {yhat})")
        conn.commit()
    time.sleep(15)
