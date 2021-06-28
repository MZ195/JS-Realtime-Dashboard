SELECT avg(price) , extract(hour from created_at) new_time 
FROM BT_Price
where created_at <= date_trunc('day',  now() + interval '1 day') and created_at >= date_trunc('day',  now())
GROUP BY new_time 
ORDER BY new_time

SELECT sum(Negative), sum(Positive) , 
extract(hour from created_at AT TIME ZONE 'UTC') new_time
FROM tweets 
WHERE created_at <= date_trunc('day',  now() + interval '1 day') AT TIME ZONE 'UTC' and created_at >= date_trunc('day',  now()) AT TIME ZONE 'UTC'
GROUP BY new_time 
ORDER BY new_time

-- SELECT COUNT(*) FROM tweets;

-- SELECT COUNT(*) FROM BT_Price;

-- SELECT COUNT(*) FROM BTC_Price_Prediction;

-- SELECT COUNT(*) FROM BTC_Price_Prediction_VARMAX;

-- SELECT COUNT(*) FROM BTC_Price_Prediction_SES;

-- SELECT * FROM BTC_Price_Prediction ORDER BY created_at DESC LIMIT 10;

-- SELECT * FROM BTC_Price_Prediction_SES ORDER BY created_at DESC LIMIT 10;

-- SELECT * FROM BTC_Price_Prediction_VARMAX ORDER BY created_at DESC LIMIT 10;

-- SELECT * FROM BTC_Price_Prediction ORDER BY created_at DESC LIMIT 10;

COPY 
	(
		SELECT to_timestamp(floor((extract('epoch' from Created_at) / 30 )) * 30) AT TIME ZONE 'UTC' time_, avg(price) ARIMA FROM 
		BTC_Price_Prediction 
		GROUP BY time_ 
		ORDER BY time_
	) 
TO '/Users/mz195/arima_predictions.csv' DELIMITER ',' CSV HEADER;

COPY 
	(
		SELECT to_timestamp(floor((extract('epoch' from Created_at) / 30 )) * 30) AT TIME ZONE 'UTC' time_, avg(price) VARMAX FROM 
		BTC_Price_Prediction_VARMAX 
		GROUP BY time_ 
		ORDER BY time_
	) 
TO '/Users/mz195/varmax_predictions.csv' DELIMITER ',' CSV HEADER;

COPY 
	(
		SELECT to_timestamp(floor((extract('epoch' from Created_at) / 30 )) * 30) AT TIME ZONE 'UTC' time_, avg(price) SES FROM 
		BTC_Price_Prediction_SES 
		GROUP BY time_ 
		ORDER BY time_
	) 
TO '/Users/mz195/ses_predictions.csv' DELIMITER ',' CSV HEADER;

COPY 
	(
		SELECT to_timestamp(floor((extract('epoch' from Created_at) / 30 )) * 30) AT TIME ZONE 'UTC' time_, avg(price) Price_avg FROM 
		BT_Price 
		GROUP BY time_ 
		ORDER BY time_
	) 
TO '/Users/mz195/BTC_price_db.csv' DELIMITER ',' CSV HEADER;