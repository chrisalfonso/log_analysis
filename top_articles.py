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

'''Building up the queries:

# 1. Get top 3 articles from LOG table. I need to strip out part of the url and just get the slug.
SELECT path, substring (path from 10) as short_slug, count(*) as views
FROM log
WHERE path not like '/'
GROUP BY path
ORDER BY views desc limit 3;

# 2. Get title of articles by joining ARTICLES and LOG tables matching on slug
SELECT articles.title, log.path
FROM articles
JOIN log on articles.slug = substring (log.path from 10) limit 3;

# Trying a subquery (edit: this works!!!):
SELECT articles.title, views
FROM (
    SELECT path, count(*) as views from log
    WHERE path not like '/'
    GROUP BY path
    ) as log_views
JOIN articles on articles.slug = substring (log_views.path from 10)
ORDER BY views desc
LIMIT 3;

# Use a view instead of subquery
CREATE VIEW article_views as
SELECT path, substring (path from 10) AS path_slug, count(*) AS views
FROM log
WHERE path like '%/article/%'
GROUP BY path;

# I've got a VIEW now, so I can fix up the above query:
SELECT articles.title, views
FROM article_views
JOIN articles on article_views.path_slug = articles.slug
ORDER BY views desc
LIMIT 3;

'''
