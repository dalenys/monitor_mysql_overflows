# monitor_mysql_overflows

####Table of contents

1. [Overview] (#overview)
2. [Usage] (#usage)
3. [Notices] (#notices)

##Overivew
This program scan and report all the TINYINT, SMALLINT, MEDIUMINT, INT, BIGINT columns where the highest value is too
close from the highest possible value allowed by the column type.

It handles UNSIGNED and SIGNED cases.

##Usage

```
./monitor.py [-u username] [-p password] [-h hostname] [-t threshold] [-e databases] [-d databases] [-h]
 - (-t) is the filling ratio threshold (ex: 0.8 for alerting when a row column value is 80% higher than tha max possible column)
 - (-e) is a comma separated list of databases to not monitor
 - (-d) is a comma separated list of databases to monitor only
``` 

##Notice
BE CAREFUL:
 - It could be very slow (especially on heavy loaded servers or servers with a huge databases/tables count.
 You surely want to run this tools on slave instead of a master
 - This script disable innodb_stats computing for optimizing performance_schema analysis and enable it at the end
 see: [http://www.percona.com/blog/2011/12/23/solving-information_schema-slowness/]