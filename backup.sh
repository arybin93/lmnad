#!/bin/bash

mysqldump=/usr/bin/mysqldump
mysql_user=root
mysql_password=root

now=$(date +"%d_%m_%Y")

$mysqldump --user=$mysql_user  --password=$mysql_password --databases lmnad_db | gzip > backup_$now.sql.gz

exit

docker cp lmnad_mysql_dev:backup_$now.sql.gz /home/ivan/lmnad-master/backup

docker exec -ti lmnad_mysql_dev rm backup_$now.sql.gz
