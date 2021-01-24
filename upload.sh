# !/bin/bash

INSTANCE=allen@ec2-13-52-212-246.us-west-1.compute.amazonaws.com
FILE_PATH=\~/cron-jobs/sf-apts/
if [ $1 == "" ]
then
    echo Must pass filename to upload!
else
    echo Uploading $1 to $FILE_PATH on $INSTANCE
    scp $1 $INSTANCE:$FILE_PATH
fi