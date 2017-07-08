# log_analysis
Analyzes database to report top articles, top authors, and frequency of HTTP errors.

## Python files

* __top_articles.py__

   Gets top 3 most popular articles, based on views

   Requires view 'article_views'

* __top_authors.py__

   Gets most popular authors, based on articles written and total number of views

   Requires view 'article_views'

* __errors.py__

   Gets days where request errors were more than 1%

   Requires the following views:
   * 'daily_errors'
   * 'daily_requests'
   * 'daily_errors_pct'

## Database views

* __article_views__
  
  CREATE VIEW article_views as
  SELECT path, substring (path from 10) AS path_slug, count(*) AS views
  FROM log
  WHERE path like '%/article/%'
  GROUP BY path;

* __daily_errors__

* __daily_errors_pct__

* __daily_requests__

