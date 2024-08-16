#!/bin/bash
timestamp=$(date +%Y-%m-%d\ \ %H:%M:%S)
git add .
git commit -m "Updated on ${timestime}"
git push
