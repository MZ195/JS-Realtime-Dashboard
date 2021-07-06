import requests
from datetime import datetime
import psycopg2
import time

conn = psycopg2.connect(database="postgres", user="postgres",
                        password="Aa@123456", host="127.0.0.1", port="5432")

URL = "https://api.coindesk.com/v1/bpi/currentprice.json"

while 1:
    r = requests.get(url=URL)
    current_time = datetime.now()
    data = r.json()
    price = data["bpi"]["USD"]["rate_float"]
    cur = conn.cursor()
    cur.execute(
        f"INSERT INTO BT_Price (Created_at,Price) VALUES ('{str(current_time)}', {price})")
    conn.commit()
    time.sleep(15)
