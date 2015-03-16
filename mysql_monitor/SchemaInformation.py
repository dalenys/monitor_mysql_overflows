import atexit
from math import ceil

from MySQLdb import escape_string


class SchemaInformation(object):
    def __init__(self, db):
        self.excluded_db = []
        self.included_db = []
        self._db = db
        self._int_types = {
            'tinyint': 255,
            'smallint': 65535,
            'mediumint': 16777215,
            'int': 4294967295,
            'bigint': 18446744073709551615}

    def init_mysql_session(self):
        cursor = self._db.cursor()
        cursor.execute('SET GLOBAL innodb_stats_on_metadata=0')
        # Handle group concat limitation (see MySQL group_concat documentation)
        cursor.execute('SET SESSION group_concat_max_len = 1048576')
        atexit.register(self.enable_statistics)

    def enable_statistics(self):
        cursor = self._db.cursor()
        cursor.execute('SET GLOBAL innodb_stats_on_metadata=1')

    def get_columns_by_table(self):

        inc_db_stmt = ''
        if self.included_db:
            inc_db_stmt = 'AND TABLE_SCHEMA IN(%s)' % self.in_stmt(
                self.included_db)

        excl_db_stmt = ''
        if self.excluded_db:
            excl_db_stmt = 'AND TABLE_SCHEMA NOT IN(%s)' % self.in_stmt(
                self.excluded_db)

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
        sql = sql % (
            inc_db_stmt, excl_db_stmt, self.in_stmt(self._int_types.keys())
        )

        cursor = self._db.cursor()
        cursor.execute(sql)

        return cursor.fetchall()

    def get_table_max_values(self, database, table, columns):
        cursor = self._db.cursor()

        max_expr = ', '.join(
            map(lambda x: 'MAX(`%s`) AS \'%s\'' % (x, x), columns)
        )
        sql = 'SELECT %s FROM %s.%s' % (max_expr, database, table)

        try:
            cursor.execute(sql)
        except Exception as error:
            print str(error)
            print sql
            exit(2)

        return cursor.fetchone()

    def in_stmt(self, l):
        return (', '.join(map(lambda x: "'" + escape_string(x) + "'", l)))

    def get_type_max_value(self, col_type, unsigned):
        if unsigned == 'unsigned':
            return self._int_types[col_type]
        else:
            return int(ceil(self._int_types[col_type] / 2))

    def _in_stmt(self, l):
        return (', '.join(map(lambda x: "'" + escape_string(x) + "'", l)))
