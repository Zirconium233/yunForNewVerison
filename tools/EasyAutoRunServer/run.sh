#!/bin/bash

# TODO: change the path to your own path
cd /path/to/yunForNewVerison/tools/EasyAutoRunServer
source /home/path_to/miniconda3/etc/profile.d/conda.sh
conda activate env

pid_file="./log/pid.txt"
echo "start" > $pid_file 

for task_file in ./configs/*.ini; do
    task_name=$(basename "$task_file" .ini)
    log_file="./log/record_${task_name}.log"
    
    nohup python ../../main.py -f="$task_file" -a -t=../../tasks_fch > "$log_file" 2>&1 &
    
    echo $! >> $pid_file
done