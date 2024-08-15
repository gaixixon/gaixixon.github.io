#!/bin/bash
cd ~/gaixixon.github.io
timestamp=$(date +%Y-%m-%d_%H:%M:%S)
sed -i -e "s/#--- Updated .*---/#--- Updated ${timestamp}  ---/g" iptv
sed -i -e "s/Updated on .*!/Updated on ${timestamp}!/g" iptv
python3 getlink.py
git add .
git commit -m "Updated on $(date +%Y-%m-%d_%H:%M:%S)"
git push
