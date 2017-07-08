import psycopg2

DBNAME = "news"

db = psycopg2.connect(database=DBNAME)	
cur = db.cursor()
query = "SELECT date, pct from daily_errors_pct WHERE pct > 1.0;"
cur.execute(query)
error_days = cur.fetchall()

print "Day(s) where request errors were more than 1 percent:"
for error_day in error_days:
	print error_day[0], "--", error_day[1], "%"

db.close()

''' Building up the queries

# 1. Get all days that had errors
SELECT path, status, time from log where status like '%404%';

# 2. Get errors by day. Do some aggregating by time (day). Gonna have to manipulate time field to extract day
SELECT date, count(*) as errors
FROM (
	SELECT time::date as date, status FROM log
	WHERE status like '%404%') as t
GROUP BY date
ORDER BY errors desc;

--> this is a view called 'daily_errors'

# 3. Get total requests per day
SELECT time::date as date, count(*) as requests FROM log
WHERE status not like '%404%'
GROUP BY date
ORDER BY requests desc;

--> this is a view called 'daily_requests'

#4. Calculate percentage by joining views
SELECT daily_requests.date, daily_errors.errors::decimal, daily_requests.requests::decimal, round(((daily_errors.errors::decimal / daily_requests.requests::decimal) * 100), 2) as pct
FROM daily_requests JOIN daily_errors 
ON daily_requests.date = daily_errors.date
ORDER BY pct desc;

--> should this be a view called 'daily_errors_pct' ?
CREATE VIEW daily_errors_pct AS
SELECT daily_requests.date, daily_errors.errors::decimal, daily_requests.requests::decimal, round(((daily_errors.errors::decimal / daily_requests.requests::decimal) * 100), 2) as pct
FROM daily_requests JOIN daily_errors 
ON daily_requests.date = daily_errors.date;

Then I could simply do:
SELECT date, pct from daily_errors_pct WHERE pct > 1.0;
