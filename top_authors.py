import psycopg2

DBNAME = "news"

db = psycopg2.connect(database=DBNAME)	
cur = db.cursor()
query = "SELECT name, sum(views) as total_views FROM (SELECT authors.name, articles.title, article_views.views FROM articles JOIN authors on articles.author = authors.id JOIN article_views on articles.slug = article_views.path_slug	ORDER BY views desc) as t GROUP BY name ORDER BY total_views desc;" 
cur.execute(query)
authors = cur.fetchall()

print "Most popular authors:"
for author in authors:
	print author[0], "--", author[1], "views"

db.close()
