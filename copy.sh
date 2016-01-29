#!/usr/bin/env bash

set -e
loc="/home/neeraj/Downloads/twitterstream-to-mongodb"
tim=$(date +"%T%D")

if [ ! -z $(pgrep twarc) ]
        then
                kill -9 $(pgrep twarc)
        fi
mv $loc/AAPL-now*.json $loc/Transfer/

twarc.py --stream AAPL &
 
