#!/bin/bash

PORT=5000
# Find the process ID (PID) that is using the port
PID=$(lsof -t -i:$PORT)

if [ -z "$PID" ]; then
    echo "No process found"
else
    kill -9 $PID
    echo "Process terminated successfully. Port is free!"
fi