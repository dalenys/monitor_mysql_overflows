#!/usr/bin/python

import MySQLdb, MySQLdb.cursors
import re
import distutils.fancy_getopt

from SchemaInformation import SchemaInformation

# TODO: Maybe monitor float types?
# TODO: Reactivate innodb stats if program is interrupted
def main():
    hostname = 'localhost'
    user = 'root'
    password = ''
    threshold = 0.8

    # TODO: maybe add phpmyadmin here?
    excluded_db = ['mysql', 'information_schema', 'performance_schema']
    included_db = []

    try:
        getopt = distutils.fancy_getopt.FancyGetopt([
            ['username=', 'u', 'MySQL username'],
            ['password=', 'p', 'MySQL password'],
            ['hostname=', 'h', 'MySQL hostname'],
            ['threshold=', 't', None,
             'The alerting threshold (ex: 0.8 means alert when a column max value is 80% of the max possible value'],
            ['exclude=', 'e', 'Database to exclude separated by a comma'],
            ['db=', 'd', 'Databases to analyse separated by a comma (default all)'],
            ['help', None, 'This help message']
        ])

        dummy, args = getopt.getopt()

    except Exception as error:
        print str(error)
        #BUG: This doesn't work
        #print "\n".join(getopt.generate_help())
        exit(2)

    if hasattr(args, 'username'): user = args.username
    if hasattr(args, 'hostname'): hostname = args.hostname
    if hasattr(args, 'password'): password = args.password
    if hasattr(args, 'threshold'): threshold = float(args.threshold)
    if hasattr(args, 'db'): included_db = args.db.split(',')
    if hasattr(args, 'exclude'): excluded_db = excluded_db + args.exclude.split(',')
    if hasattr(args, 'help'):
        #BUG: this doesn't works
        #print "\n".join(getopt.generate_help())
        exit(2)

    # MySQL connection
    db = MySQLdb.connect(host=hostname, user=user, passwd=password, cursorclass=MySQLdb.cursors.DictCursor)

    # Configure schma analyser
    schema = SchemaInformation(db)
    schema.excludeDatabases(excluded_db)

    if included_db: schema.includeDatabases(included_db)

    # Disabling InnoDB statistics for performances
    schema.disableStatistics()

    # Get column definitions
    columns = schema.getColumnsByTable()

    for definition in columns:
        # Get all max values for a given table
        columns_max_values = schema.getTableMaxValues(definition['TABLE_SCHEMA'], definition['TABLE_NAME'],
                                                      definition['COLUMN_NAMES'].split(','))

        column_names = definition['COLUMN_NAMES'].split(',')
        column_types = definition['COLUMN_TYPES'].split(',')

        idx = 0
        for name in column_names:
            # Parsing column data to retrieve details, max values ...
            full_type = column_types[idx]
            type, unsigned = re.split('\\s*\(\d+\)\s*', full_type)
            max_allowed = schema.getTypeMaxValue(type, unsigned)
            current_max_value = columns_max_values[name]

            # Calculate max values with threshold and comparing
            if (current_max_value >= int(max_allowed * threshold)):
                percent = round(float(current_max_value) / float(max_allowed) * 100, 2)
                resting = max_allowed - current_max_value
                print "WARNING: (%s %s) %s.%s.%s max value is %s near (allowed=%s%%, resting=%s)" % (
                    type, unsigned, definition['TABLE_SCHEMA'], definition['TABLE_NAME'], name, current_max_value,
                    percent, resting)

            idx += 1
    schema.enableStatistics()

    db.close()


print "Start"
main()
print "Done"

