import psycopg2

DBNAME = "news"

db = psycopg2.connect(database=DBNAME)	
cur = db.cursor()
query = "SELECT articles.title, views FROM article_views JOIN articles on article_views.path_slug = articles.slug ORDER BY views desc LIMIT 3;"
cur.execute(query)
articles = cur.fetchall()

print "Top 3 Articles"
for article in articles:
	print article[0], "--", article[1], "views"

db.close()
