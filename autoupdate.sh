#!/bin/bash
cd ~/tv360/gaixixon.github.io
python3 ~/tv360/gaixixon.github.io/getlink.py
#sleep 15
git add .
git commit -m 'Update on $(date +"%Y-%m-%d")'
git push
