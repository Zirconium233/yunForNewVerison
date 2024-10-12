#!/bin/bash

# TODO: change the path to your own path
cd /home/zhangran/desktop/test_background_task/new_yun/yunForNewVerison/tools/EasyAutoRunServer
source /home/zhangran/miniconda3/etc/profile.d/conda.sh
conda activate py310

pid_file="./log/pid.txt"
echo "start" > $pid_file 

for task_file in ./configs/*.ini; do
    task_name=$(basename "$task_file" .ini)
    log_file="./log/record_${task_name}.log"
    
    nohup python ../../main.py -f="$task_file" -a -t=../../tasks_fch > "$log_file" 2>&1 &
    
    echo $! >> $pid_file
done