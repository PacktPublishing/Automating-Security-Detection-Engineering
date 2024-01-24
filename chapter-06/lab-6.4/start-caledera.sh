#!/usr/bin/bash
cd /home/dc/Downloads/caldera
python3 server.py --insecure &
sleep 10
#use default sandcat agent
server="http://0.0.0.0:8888";curl -s -X POST -H "file:sandcat.go" -H "platform:linux" $server/file/download > splunkd;chmod +x splunkd;./splunkd -server $server -group red -v &
