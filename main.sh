#!/bin/bash
file_path="opt/render/zipper/zipper.py"
echo $pwd
# Replace all occurrences of /home/u209464/Work with opt/render in the file
sed -i 's#/home/u209464/Work#opt/render#g' $file_path
# Define an array of process names and their corresponding commands
declare -A processes
processes["zipper.py"]="nohup python3 /opt/render/zipper/zipper.py &"
# Declare an associative array to track process PIDs
declare -A pids
pip install --upgrade pip

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

