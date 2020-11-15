#!/bin/bash

smart_house_script_file=syslog_catcher.py
smart_house_script_path=/home/stastodd/projects/smart_house/
smart_house_script_pid=$(ps -axx | grep smart_house | grep syslog_catcher.py | awk '{print $1}')

if [ $smart_house_script_pid ]
  then
    echo "smart_house script is running, it have pid: $smart_house_script_pid"
  else
    cd $smart_house_script_path ; ./$smart_house_script_file &
fi

