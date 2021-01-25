#!/usr/bin/env bash

DIR=/home/allen/cron-jobs/sf-apts 
HOME=/root 
LOGNAME=root 
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin 
LANG=en_US.UTF-8 
SHELL=/bin/sh 
PWD=/root 
cd $DIR 
$DIR/env/bin/python 
$DIR/scraper.py cp 
$DIR/PriceLog.txt /var/www/html/
