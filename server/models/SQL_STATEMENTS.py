import psycopg2
import warnings


def setup():
    # Ignore warnings
    warnings.filterwarnings("ignore")

    # Create database connection
    conn = psycopg2.connect(database="postgres", user="postgres",
                            password="Aa@123456", host="127.0.0.1", port="5432")

    return conn


BTC_PRICE_1_HOUR_WINDOW = '''SELECT to_timestamp(floor((extract('epoch' from Created_at) / 30 )) * 30) AT TIME ZONE 'UTC' time_ , avg(price) price_
                                FROM BT_Price
                                WHERE created_at <= date_trunc('hour',  now() + interval '1 hour') and created_at >= (now() - interval '1 hour')
                                GROUP BY time_
                                ORDER BY time_'''

TWEETS_1_HOUR_WINDOW = '''SELECT to_timestamp(floor((extract('epoch' from Created_at) / 30 )) * 30) time_ , COUNT(*)
                                FROM tweets
                                WHERE created_at <= date_trunc('hour',  now() + interval '1 hour') AT TIME ZONE 'UTC' and created_at >= (now() - interval '1 hour') AT TIME ZONE 'UTC'
                                GROUP BY time_
                                ORDER BY time_'''
