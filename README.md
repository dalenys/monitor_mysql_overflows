# monitor_mysql_overflows

#### Table of contents

1. [Overview] (#Overview)
2. [Usage] (#Usage)
3. [Notices] (#Notices)

## Overview
This program scan and report all the TINYINT, SMALLINT, MEDIUMINT, INT, BIGINT columns where the highest value is too
close from the highest possible value allowed by the column type.

It handles UNSIGNED and SIGNED cases.

## Usage

```
usage: monitor.py [-h] [--username USERNAME] [--password [PASSWORD]]
                  [--host HOST] [--threshold THRESHOLD]
                  [--exclude EXCLUDE [EXCLUDE ...]] [--db DB [DB ...]]

optional arguments:
  -h, --help            show this help message and exit
  --username USERNAME, -u USERNAME
                        MySQL username
  --password [PASSWORD], -p [PASSWORD]
                        MySQL password
  --host HOST           MySQL host
  --threshold THRESHOLD, -t THRESHOLD
                        The alerting threshold (ex: 0.8 means alert when a
                        column max value is 80% of the max possible value
  --exclude EXCLUDE [EXCLUDE ...], -e EXCLUDE [EXCLUDE ...]
                        Database to exclude separated by a comma
  --db DB [DB ...], -d DB [DB ...]
                        Databases to analyse separated by a comma (default
                        all)
``` 

## Notices
BE CAREFUL:
 - It could be very slow (especially on heavy loaded servers or servers with a huge databases/tables count.
 You surely want to run this tools on slave instead of a master
 - This script disable innodb_stats computing for optimizing performance_schema analysis and enable it at the end
 see: [http://www.percona.com/blog/2011/12/23/solving-information_schema-slowness/]