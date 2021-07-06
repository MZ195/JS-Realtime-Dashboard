import requests
import pandas as pd
from datetime import datetime
import psycopg2
import time
from sklearn.ensemble import RandomForestRegressor

conn = psycopg2.connect(database="postgres", user="postgres",
                        password="Aa@123456", host="127.0.0.1", port="5432")

ARIMA_URL = "http://localhost:9000/predict/ARIMA"
VARMAX_URL = "http://localhost:9000/predict/VARMAX"
SES_URL = "http://localhost:9000/predict/SES"
ACTUAL_URL = "http://localhost:9000/btc/price"


while 1:
    actual_res = requests.get(url=ACTUAL_URL)
    actual_data = actual_res.json()

    ARIMA_res = requests.get(url=ARIMA_URL)
    ARIMA_data = ARIMA_res.json()[:-2]

    VARMAX_res = requests.get(url=VARMAX_URL)
    VARMAX_data = VARMAX_res.json()[:-2]

    SES_res = requests.get(url=SES_URL)
    SES_data = SES_res.json()[:-2]

    actual = pd.DataFrame.from_dict(actual_data)
    actual.columns = ['datetime', 'PRICE']

    arima = pd.DataFrame.from_dict(ARIMA_data)
    arima.columns = ['datetime', 'ARIMA']

    varmax = pd.DataFrame.from_dict(VARMAX_data)
    varmax.columns = ['datetime', 'VARMAX']

    ses = pd.DataFrame.from_dict(SES_data)
    ses.columns = ['datetime', 'SES']

    arima_df = actual.merge(arima, on='datetime')
    arima_varmax_df = arima_df.merge(varmax, on='datetime')
    all_models_df = arima_varmax_df.merge(ses, on='datetime')

    X = all_models_df.drop(["datetime", "PRICE"], axis=1)
    y = all_models_df.PRICE

    reg_forest = RandomForestRegressor(n_estimators=100, criterion='mse')

    reg_forest.fit(X, y)

    ARIMA_preds = ARIMA_res.json()[-2:]
    VARMAX_preds = VARMAX_res.json()[-2:]
    SES_preds = SES_res.json()[-2:]

    for i in range(len(ARIMA_preds)):
        arima_pred = ARIMA_preds[i]["price"]
        varmax_pred = VARMAX_preds[i]["price"]
        ses_pred = SES_preds[i]["price"]

        current_time_str = ARIMA_preds[i]["datetime"].split(":")

        current_time = datetime.now()
        current_time = current_time.replace(
            hour=int(current_time_str[0]), minute=int(current_time_str[1]), second=int(current_time_str[2]), microsecond=0)

        if abs(arima_pred - varmax_pred) > 200:
            res1 = ((arima_pred) + (ses_pred))/2
            res2 = reg_forest.predict(
                [[arima_pred, all_models_df["PRICE"].mean(), ses_pred]])[0]
        else:
            res1 = ((arima_pred) + (varmax_pred) + (ses_pred))/3
            res2 = reg_forest.predict([[arima_pred, varmax_pred, ses_pred]])[0]

        cur = conn.cursor()
        cur.execute(
            f"INSERT INTO BTC_Price_Prediction_RF (Created_at,Price) VALUES ('{str(current_time)}', {res2})")
        conn.commit()
        res = (res1 + (res2))/2

        cur = conn.cursor()
        cur.execute(
            f"INSERT INTO BTC_Price_Prediction_Overall (Created_at,Price) VALUES ('{str(current_time)}', {res})")
        conn.commit()
    time.sleep(15)
