#!/bin/bash
#kill -15 $(ps aux | grep python3 | grep -v grep | awk '{print $2}')

#ps aux | grep python3 | grep -v grep | awk '{print $2}' | while read pid; do
#    kill -15 "$pid"
#done


sudo ps aux | grep python3 | grep -v grep | awk '{print $2}' | xargs kill -15

#cd ~/iptv
#python3 iptv.py -u 2>>/tmp/http_request.log &
sudo nohup python3 /home/ec2-user/https/server.py -u 2>>/tmp/https.log &

sudo nohup python3 /home/ec2-user/iptv/iptv.py -u 2>>/dev/null &
