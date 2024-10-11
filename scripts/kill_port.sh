#!/bin/bash

PORT=$1

PID=$(lsof -i :$PORT -t | awk '{print $2}')
if [ -n "$PID" ]; then
  kill -9 $PID
  echo "Process $PID terminated."
else
  echo "No process found using port $PORT."
fi