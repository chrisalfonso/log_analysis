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
