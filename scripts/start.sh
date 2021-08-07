#!/bin/bash
cd /data
echo "Fetching server files"
curl -o altitude.tar.bz2 https://nimblygames-installers.s3.amazonaws.com/altitude.tar.bz2 
tar -xf altitude.tar.bz2

echo "Building configuration file from environment"
/scripts/build_config.py /config env_config.xml /data/config.xml

echo "Launching Server"
./bin/server_launcher -config /data/config.xml
