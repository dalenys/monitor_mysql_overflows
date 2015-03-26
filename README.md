# mysql-monitor

#### Table of contents

1. [Overview] (#overview)
2. [Usage] (#usage)
3. [Notices] (#notices)
4. [Installation] (#installation)
5. [Development] (#development)

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
 You surely want to run this tool on a slave instead of a master

 - This script disable innodb_stats computing for optimizing performance_schema analysis and enable it at the end

 See: http://www.percona.com/blog/2011/12/23/solving-information_schema-slowness/

 If you interrupt this script (Ctrl+C ...) it is up to you to reactivate it using something like:
 set global innodb_stats_on_metadata=1;


## Installation

To install it with a [Python virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/) (recommended):

```
$> virtualenv myenv
$> source myenv/bin/activate
(myenv) $> pip install mysql-monitor
(myenv) $> mysql-monitor -h
```

Or on your system, without virtualenv:

```
$> pip install mysql-monitor
$> mysql-monitor -h
```

## Development

To start hacking on the project, run:

```
$> virtualenv myenv
$> source myenv/bin/activate
(myenv) $> pip install -e .
(myenv) $> mysql-monitor -h
```
