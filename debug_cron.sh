#!/bin/bash

# send the CRON entries from the syslog to a local log file to debug
grep CRON /var/log/syslog >> /home/pi/guitar_search/logs/cronlogs.log

# tell user where to find it
echo "appended info to /home/pi/guitar_search/logs/cronlogs.log"

