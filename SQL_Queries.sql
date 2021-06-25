
SELECT now() - interval '30 minute'

select date_trunc('day',  now() + interval '1 day')

SELECT date_trunc('hour',  now() + interval '1 hour')

SELECT created_at AT TIME ZONE 'UTC'
FROM tweets 
ORDER BY created_at DESC
LIMIT 10
-- WHERE Created_at >= date_trunc('hour',  now() - interval '3 hour')

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

select * from tweets LIMIT 10;

select * from BT_Price;

select count(*) from BT_Price;

select count(*) from tweets;


SELECT avg(price) , to_timestamp(floor((extract('epoch' from Created_at) / 30 )) * 30) new_time FROM BT_Price GROUP BY new_time ORDER BY new_time

COPY (SELECT avg(price) , to_timestamp(floor((extract('epoch' from Created_at) / 30 )) * 30) new_time FROM BT_Price GROUP BY new_time ORDER BY new_time) TO '/Users/mz195/BT_PriceDB.csv' DELIMITER ',' CSV HEADER;

COPY (SELECT sum(Negative) neg , sum(Positive) pos, to_timestamp(floor((extract('epoch' from Created_at AT TIME ZONE 'UTC') / 30 )) * 30)  new_time FROM tweets GROUP BY new_time ORDER BY new_time) TO '/Users/mz195/tweets_db.csv' DELIMITER ',' CSV HEADER;
	
--select to_timestamp(floor((extract('epoch' from Created_at) / 30 )) * 30) AT TIME ZONE 'UTC' new_time from BT_Price;

-- SELECT avg(price) , to_timestamp(floor((extract('epoch' from Created_at) / 30 )) * 30) new_time 
-- FROM BT_Price
-- where created_at <= date_trunc('hour',  now() + interval '1 hour') and created_at >= date_trunc('hour',  now())
-- GROUP BY new_time 
-- ORDER BY new_time;

--CREATE TABLE BT_Price(
  -- ID_ SERIAL,
   --created_at TIMESTAMP,
  -- price float);