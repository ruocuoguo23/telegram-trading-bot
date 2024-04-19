#!/bin/bash

# Name of the main Python script without the .py extension
SCRIPT_NAME="trading_bot"

# Use pgrep to find the process ID (PID) of the Python script
# The -f flag is used to search for the full command line
# The name of the script is used to find the correct process
PID=$(pgrep -f $SCRIPT_NAME)

# Check if the PID variable is set (i.e., if the process was found)
if [ -z "$PID" ]; then
    echo "The process $SCRIPT_NAME does not appear to be running."
    exit 1
else
    # Kill the process
    kill "$PID"
    echo "Process $SCRIPT_NAME with PID $PID has been stopped."
fi
