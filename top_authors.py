import psycopg2

DBNAME = "news"

db = psycopg2.connect(database=DBNAME)
cur = db.cursor()
query = "SELECT name, sum(views) as total_views \
(SELECT authors.name, articles.title, article_views.views \
FROM articles JOIN authors on articles.author = authors.id \
JOIN article_views on articles.slug = article_views.path_slug \
ORDER BY views desc) as t \
GROUP BY name ORDER BY total_views desc;"
cur.execute(query)
authors = cur.fetchall()

print "Most popular authors:"
for author in authors:
	print author[0], "--", author[1], "views"

db.close()

''' Building up the queries
# 1. Get author names and titles of articles they've written
SELECT authors.name, articles.title FROM articles
JOIN authors on articles.author = authors.id
ORDER BY authors.name;

# I think I'm going to need a view to list the number of article views:
CREATE VIEW article_views AS
SELECT path, substring (path from 10) as path_slug, count(*) as views
FROM log
WHERE path like '%/article/%'
GROUP BY path

(note: leave "ORDER BY views desc" to the outer query)

# 2. Get author names, titles of articles they've written and \
    the views of the individual articles
SELECT authors.name, articles.title, article_views.views FROM articles
JOIN authors on articles.author = authors.id
JOIN article_views on articles.slug = article_views.path_slug
ORDER BY views desc;

# 3. Building off of #2, aggregate the views and show who has the most!
SELECT name, sum(views) as total_views
FROM (
    SELECT authors.name, articles.title, article_views.views FROM articles
    JOIN authors on articles.author = authors.id
    JOIN article_views on articles.slug = article_views.path_slug
    ORDER BY views desc) as t
GROUP BY name
ORDER BY total_views desc;

'''
