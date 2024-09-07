#!/bin/bash
kill -15 $(ps aux | grep python3 | grep -v grep | awk '{print $2}')
cd ~/iptv
python3 iptv.py -u 2>/tmp/http_request.log &

