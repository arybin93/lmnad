#!/bin/bash

mysqldump=/usr/bin/mysqldump
mysql_user=root
mysql_password=root

now=$(date +"%d_%m_%Y")

docker exec -i lmnad_mysql_dev $mysqldump --user=$mysql_user  --password=$mysql_password --databases lmnad_db | gzip > backup/backup_$now.sql.gz

