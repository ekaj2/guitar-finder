#!/bin/bash

# log what's going on (append with >>)
date >> /tmp/my_cron.log
echo "checking for guitars" >> /tmp/my_cron.log

# run python script
python3 /home/pi/guitar_search/guitar_center_parser.py

