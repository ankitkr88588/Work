#!/bin/bash

# Define an array of process names and their corresponding commands
declare -A processes
processes["magisk.py"]="nohup python3 /home/u201900/Magisk-flasher/main.py &"
processes["whisper.py"]="nohup python3 /home/u201900/main3.py &"
processes["firmware.py"]="nohup python3 /home/u201900/firmware/firmware.py &"
# Declare an associative array to track process PIDs
declare -A pids

# Monitor and restart processes
while true; do
    for process_name in "${!processes[@]}"; do
        # Get the PID of the process
        pid="${pids[$process_name]}"

        if [[ -z "$pid" ]] || ! kill -0 "$pid" 2>/dev/null; then
            echo "Starting $process_name..."
            eval "${processes[$process_name]}"
            # Store the PID of the newly started process
            pids["$process_name"]="$!"
        fi
    done
    sleep 1
done

