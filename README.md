# log_analysis
Analyzes database to report top articles, top authors, and frequency of HTTP errors.

top_articles.py
Gets top 3 most popular articles, based on views

Requires view 'article_views'

top_authors.py
Gets most popular authors, based on articles written and total number of views

Requires view 'article_views'

errors.py
Gets days where request errors were more than 1%

Requires the following views:
'daily_errors'
'daily_requests'
'daily_errors_pct'


