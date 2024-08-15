#!/bin/bash
cd ~/gaixixon.github.io
now = $(date +%Y-%m-%d %H:%M:%S)
sed -i -e 's/#--- Updated .*---/#--- Updated $(now)---/' iptv
python3 getlink.py
#sleep 15
git add .
git commit -m "Updated on $(date +%Y-%m-%d_%H:%M:%S)"
git push
