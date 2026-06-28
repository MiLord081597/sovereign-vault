#!/bin/zsh

echo "====================================="
echo " INITIATING LIVE INGESTION LOOP      "
echo " PRESS CTRL+C TO TERMINATE STREAM    "
echo "====================================="
sleep 1

while true; do
    TIMESTAMP=$(date +"%H:%M:%S")
    echo "[$TIMESTAMP] BAXTER CORE: Ingesting 888 Hz harmonized pulse... [STABLE]"
    sleep 2
done
