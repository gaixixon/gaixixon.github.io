#!/bin/bash
cd ~/gaixixon.github.io
timestamp=$(date +%Y-%m-%d_%H:%M:%S)
sed -i -e 's/#--- Updated .*---/#--- Updated ${date +%Y-%m-%d_%H:%M:%S} ---/' iptv
python3 getlink.py
#sleep 15
git add .
git commit -m "Updated on $(date +%Y-%m-%d_%H:%M:%S)"
git push
