#!/bin/bash

# convert a tab file to csv file
# arg1 : tab file to convert
# arg2 : destination file
# sample : "tab2csv.sh
#           /var/www/html/porn-dataviz/dataset/original/youporn/video-comments-and-usernames-clean.001.tab
#           /var/www/html/porn-dataviz/dataset/generated/youporn/video-comments-and-usernames-clean.001"
# author : martin

if [ -z "$1" ] || [ -z "$2" ]; then
    echo "No arguments supplied"
    exit 1
fi

sed 's/|/ /g' $1 | sed 's/"\t"/"|"/g' | sed 's/"//g' > "$2".csv