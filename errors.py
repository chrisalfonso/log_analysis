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


troubleshooting:
--> I need to divide the daily_errors.errors column values by daily_requests.requests column values. All I'm getting now is '0'

----> maybe I need to cast the values to numeric? decimal?
https://dba.stackexchange.com/questions/69108/postgresql-using-count-to-determine-percentages-cast-issues

2017-07-7: I did it! cast value to decimal, move the decimal and round 2 places.


Notes:
- I could probably do this as a subquery? SELF JOIN?


'''

'''
# For a more advanced app later on?
def freq_errors():
	# On which days did more than 1% of requests lead to errors
	db = psycopg2.connect(database=DBNAME)
	cur = db.cursor()
	cur.execute()
	errors = cursor.fetchall()
	db.close()
	return errors
'''
