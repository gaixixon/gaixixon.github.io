#!/bin/bash
cd ~/gaixixon.github.io
git pull
timestamp=$(date +%Y-%m-%d_%H:%M:%S)
sed -i -e "s/#--- Updated .*---/#--- Updated ${timestamp}  ---/g" iptv
sed -i -e "s/Updated on .*!/Updated on ${timestamp}!/g" iptv
#python3 getlink.py
python3 tv360.py
git add .
git commit -m "Updated on $(date +%Y-%m-%d_%H:%M:%S)"
git push
