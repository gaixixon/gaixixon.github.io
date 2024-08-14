#!/bin/bash
cd ~/tv360/gaixixon.github.io
python3 ~/tv360/gaixixon.github.io/getlink.py
#sleep 15
git add .
git commit -m "Updated on $(date +%Y-%m-%d_%H:%M:%S)"
git push
