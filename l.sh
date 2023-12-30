#!/bin/bash

# Function to submit the job and get the job ID
submit_job() {
<<<<<<< HEAD
    job_id=$(qsub -l nodes=1:gpu:ppn=2,walltime=24:00:00 -d . main.sh)
    echo "Job submitted with ID: $job_id"
}
submit_job
=======
    job_id=$(qsub main.sh)
    echo "Job submitted with ID: $job_id"
}

>>>>>>> 452c8fa3a5220a0785b60fbf3804bbeb6de4a8df
# Function to check if the job is still in the queue or running
job_is_running() {
    job_status=$(qstat -u $USER | awk -v job_id="$1" '$1 == job_id {print $5}')
    [ "$job_status" == "R" ] || [ "$job_status" == "Q" ]
}

# Submit the initial job
<<<<<<< HEAD
=======
submit_job
>>>>>>> 452c8fa3a5220a0785b60fbf3804bbeb6de4a8df

# Continuously monitor the job
while true; do
    if ! job_is_running "$job_id"; then
        echo "Job with ID $job_id has completed."
        # Restart the job
<<<<<<< HEAD
        qdel all
        submit_job
    fi
    sleep 86400  # Adjust the polling interval (in seconds) as needed
=======
        submit_job
    fi
    sleep 60  # Adjust the polling interval (in seconds) as needed
>>>>>>> 452c8fa3a5220a0785b60fbf3804bbeb6de4a8df
done

