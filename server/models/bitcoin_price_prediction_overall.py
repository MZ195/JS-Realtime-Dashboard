import requests
import pandas as pd
from datetime import datetime
import psycopg2
import time

conn = psycopg2.connect(database="postgres", user="postgres",
                        password="Aa@123456", host="127.0.0.1", port="5432")

ARIMA_URL = "http://localhost:9000/predict/ARIMA"
VARMAX_URL = "http://localhost:9000/predict/VARMAX"
SES_URL = "http://localhost:9000/predict/SES"
RF_URL = "http://localhost:9000/predict/RF"
ACTUAL_URL = "http://localhost:9000/btc/price"


while 1:
    actual_res = requests.get(url=ACTUAL_URL)
    actual_data = actual_res.json()

    ARIMA_res = requests.get(url=ARIMA_URL)
    ARIMA_preds = ARIMA_res.json()[-2:]

    VARMAX_res = requests.get(url=VARMAX_URL)
    VARMAX_preds = VARMAX_res.json()[-2:]

    SES_res = requests.get(url=SES_URL)
    SES_preds = SES_res.json()[-2:]

    RF_res = requests.get(url=RF_URL)
    RF_preds = RF_res.json()[-2:]

    for i in range(len(ARIMA_preds)):
        arima_pred = ARIMA_preds[i]["price"]
        varmax_pred = VARMAX_preds[i]["price"]
        ses_pred = SES_preds[i]["price"]
        rf_pred = RF_preds[i]["price"]

        current_time_str = ARIMA_preds[i]["datetime"].split(":")

        current_time = datetime.now()
        current_time = current_time.replace(
            hour=int(current_time_str[0]), minute=int(current_time_str[1]), second=int(current_time_str[2]), microsecond=0)

        if abs(arima_pred - varmax_pred) > 200:
            # to handle the case when both the website & API are down
            res = ((arima_pred) + (ses_pred) + (rf_pred))/3
        else:
            res = ((arima_pred) + (varmax_pred) + (ses_pred) + (rf_pred))/4
        cur = conn.cursor()
        cur.execute(
            f"INSERT INTO BTC_Price_Prediction_Overall (Created_at,Price) VALUES ('{str(current_time)}', {res})")
        conn.commit()
    time.sleep(15)
