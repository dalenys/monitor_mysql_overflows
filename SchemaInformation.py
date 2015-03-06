import MySQLdb
import math


class SchemaInformation:
    def __init__(self, db):
        self.db = db
        self._excluded_db = []
        self._included_db = []
        self._int_types = {
            'tinyint': 255,
            'smallint': 65535,
            'mediumint': 16777215,
            'int': 4294967295,
            'bigint': 18446744073709551615}

    def includeDatabases(self, databases):
        self._included_db = databases

    def excludeDatabases(self, databases):
        self._excluded_db = databases

    def disableStatistics(self):
        cursor = self.db.cursor()
        cursor.execute('SET GLOBAL innodb_stats_on_metadata=0')

    def enableStatistics(self):
        cursor = self.db.cursor()
        cursor.execute('SET GLOBAL innodb_stats_on_metadata=1')

    def getColumnsByTable(self):

        if self._included_db:
            incDbStmt = 'AND TABLE_SCHEMA IN(%s)' % self.inStmt(self._included_db)
        else:
            incDbStmt = ''

        if self._excluded_db:
            exclDbStmt = 'AND TABLE_SCHEMA NOT IN(%s)' % self.inStmt(self._excluded_db)
        else:
            exclDbStmt = ''

        sql = """
SELECT
  TABLE_SCHEMA,
  TABLE_NAME,
  GROUP_CONCAT(COLUMN_NAME) AS COLUMN_NAMES,
  GROUP_CONCAT(COLUMN_TYPE) AS COLUMN_TYPES
FROM information_schema.COLUMNS
WHERE 1
    %s
    %s
    AND DATA_TYPE IN (%s)
GROUP BY TABLE_SCHEMA, TABLE_NAME
ORDER BY TABLE_SCHEMA, TABLE_NAME, COLUMN_NAME
"""
        sql = sql % (incDbStmt, exclDbStmt, self.inStmt(self._int_types.keys()))

        cursor = self.db.cursor()
        cursor.execute(sql)

        return cursor.fetchall()

    def getTableMaxValues(self, database, table, columns):
        cursor = self.db.cursor()

        max = ', '.join(map(lambda x: 'MAX(%s) AS %s' % (x, x), columns))
        sql = 'SELECT %s FROM %s.%s' % (max, database, table)

        cursor.execute(sql)

        return cursor.fetchone()

    def inStmt(self, l):
        return (', '.join(map(lambda x: "'" + MySQLdb.escape_string(x) + "'", l)))

    def getTypeMaxValue(self, type, unsigned):
        if unsigned == 'unsigned':
            return self._int_types[type]
        else:
            return int(math.ceil(self._int_types[type] / 2))



