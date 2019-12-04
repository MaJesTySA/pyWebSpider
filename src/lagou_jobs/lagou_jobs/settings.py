BOT_NAME = 'lagou_jobs'

SPIDER_MODULES = ['lagou_jobs.spiders']
NEWSPIDER_MODULE = 'lagou_jobs.spiders'

ROBOTSTXT_OBEY = False
COOKIES_ENABLE = True
COOKIES_DEBUG = True
MYSQL_HOST = '127.0.0.1'
MYSQL_DBNAME = 'lagou_jobs'
MYSQL_USER = 'root'
MYSQL_PWD = 'z55182182'
SQL_DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
SQL_DATE_FORMAT = '%Y-%m-%d'

DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
}

ITEM_PIPELINES = {
   'lagou_jobs.pipelines.AsyncMySQLPipeline': 300,
}

