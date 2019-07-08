#!/bin/bash

bak_dir=("/data01/nmjf/chenteng/bak")  # 可增加多个目录
date1=`date -d "-2 day" +"%Y%m%d"`
date2=`date -d "-1 day" +"%Y%m%d"`
date3=`date +"%Y%m%d"`

for dir in ${bak_dir[@]}
do
    dir_list=`ls $dir | grep -v -e $date1 -e $date2 -e $date3` 
   
    cd $dir > /dev/null
    for recordDir in $dir_list
    do
        rm -fr $recordDir > /dev/null
    done
done
