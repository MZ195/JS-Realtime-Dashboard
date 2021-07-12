import pandas as pd
from datetime import datetime, timedelta
from statsmodels.tsa.holtwinters import SimpleExpSmoothing
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


def predict_SES():
    conn = SQL_STATEMENTS.setup()

    while(1):
        cur = conn.cursor()
        cur.execute(SQL_STATEMENTS.BTC_PRICE_1_HOUR_WINDOW)
        rows = cur.fetchall()
        conn.commit()

        df = pd.DataFrame(rows, columns=['time', 'price'])
        history = [x for x in df["price"].values]

        for i in range(0, 2):
            current_time = datetime.now() + timedelta(seconds=(i * 30))
            model = SimpleExpSmoothing(history)
            model_fit = model.fit()
            output = model_fit.forecast()
            yhat = output[0]

            newdatetime = date_formating(current_time)

            history.append(yhat)
            cur = conn.cursor()
            cur.execute(
                f"INSERT INTO BTC_Price_Prediction_SES (created_at,price) VALUES ('{str(newdatetime)}', {yhat})")
            conn.commit()
        time.sleep(15)
