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
  
  ```
  CREATE VIEW article_views AS
  SELECT path, substring (path from 10) AS path_slug, count(*) AS views
  FROM log
  WHERE path like '%/article/%'
  GROUP BY path;
  ```

* __daily_errors__

  ```
  CREATE VIEW daily_errors AS
  SELECT date, count(*) as errors
  FROM (
	SELECT time::date as date, status FROM log
	WHERE status like '%404%') as t
  GROUP BY date
  ORDER BY errors desc;
  ```

* __daily_requests__

  ```
  CREATE VIEW daily_requests AS
  SELECT time::date as date, count(*) as requests FROM log
  WHERE status not like '%404%'
  GROUP BY date
  ORDER BY requests desc;
  ```

* __daily_errors_pct__

  ```
  CREATE VIEW daily_errors_pct AS
  SELECT daily_requests.date, round(((daily_errors.errors::decimal / daily_requests.requests::decimal) * 100), 2) as pct
  FROM daily_requests JOIN daily_errors 
  ON daily_requests.date = daily_errors.date;
  ```
