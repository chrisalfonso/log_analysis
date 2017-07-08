# log_analysis
Analyzes database to report top articles, top authors, and frequency of HTTP errors.

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

* __newsdata.sql__ 

  Tables: articles, authors, log
  Views: article_views, daily_errors, daily_errors_pct, daily_requests
