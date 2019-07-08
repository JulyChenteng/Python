#!/bin/bash

now=`date +"%Y-%m-%d %H-%M-%S"`
day=`date +"%Y%m%d"`
ps -ef | grep pack.py | grep -v grep

if [ $? -ne 0 ] 
then
    python /xzbilldata01/billapp/scripts/tools/pack.py >> /xzbilldata01/billapp/log/pack.log.$day
    echo "$now, Success: start python pack.py......" >> /xzbilldata01/billapp/log/pack_process.log
else
    echo "$now, Exception: python pack.py is running......" >> /xzbilldata01/billapp/log/pack_process.log
fi
    