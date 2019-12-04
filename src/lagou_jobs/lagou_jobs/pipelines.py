from twisted.enterprise import adbapi

class AsyncMySQLPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        from MySQLdb.cursors import DictCursor
        dbparams = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PWD'],
            charset='utf8mb4',
            cursorclass=DictCursor,
            use_unicode=True
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbparams)
        return cls(dbpool)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.hand_error, item, spider)

    def do_insert(self, cursor, item):
        insert_sql, params = item.get_insert_sql()
        cursor.execute(insert_sql, params)


    def hand_error(self, failure, item, spider):
        print(failure)