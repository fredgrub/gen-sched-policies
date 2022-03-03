from __future__ import print_function
import numpy as np
import re
import random
import subprocess
import sys
import os.path
import time

filename = "lublin_256.swf"

model_num_nodes = []
model_run_times = []
model_submit_times = []
num_tasks_queue = 32
num_tasks_state = 16
earliest_submit = 0
tasks_state_nodes = []
tasks_state_runtimes = []
tasks_state_submit = []
tasks_queue_nodes = []
tasks_queue_runtimes = []
tasks_queue_submit = []

all_trials = [
    int(1E3), int(2E3), int(4E3), int(8E3), int(16E3),
    int(32E3), int(64E3), int(128E3), int(256E3), int(512E3)
    ]

#all_trials = [int(1E3), int(2E3)]

random.seed(1234) # reproducibility 

# create tuple (S,Q)
with open(filename) as f:
    for line in f.readlines():
        row = re.split(" +", line.lstrip(" "))
        if row[0] == ';':
            continue
        #print("%f %d" % (float(row[4]), int(row[5])))  
        if int(row[4]) > 0 and int(row[4]) <= 256 and int(row[3]) > 0:
            model_run_times.append(int(row[3]))
            model_num_nodes.append(int(row[4]))
            model_submit_times.append(int(row[1])) 

with open("task-sets/set-test.csv", "w+") as task_file:
    tasks_state_nodes = []
    tasks_state_runtimes = []
    tasks_state_submit = []
    choose = random.randint(0,len(model_run_times)-1 - (num_tasks_queue+num_tasks_state))
    earliest_submit = model_submit_times[choose]
    for j in xrange(0,16):
        tasks_state_nodes.append(model_num_nodes[choose+j])
        tasks_state_runtimes.append(model_run_times[choose+j])
        tasks_state_submit.append(model_submit_times[choose+j] - earliest_submit)
        task_file.write(str(tasks_state_runtimes[j])+","+str(tasks_state_nodes[j])+","+str(tasks_state_submit[j])+"\n")
    tasks_queue_nodes = []
    tasks_queue_runtimes = []
    tasks_queue_submit = []
    for j in xrange(0,32):
        #choose = random.randint(0,len(model_run_times)-1)
        tasks_queue_nodes.append(model_num_nodes[num_tasks_state+choose+j])
        tasks_queue_runtimes.append(model_run_times[num_tasks_state+choose+j])
        tasks_queue_submit.append(model_submit_times[num_tasks_state+choose+j] - earliest_submit)
        task_file.write(str(tasks_queue_runtimes[j])+","+str(tasks_queue_nodes[j])+","+str(tasks_queue_submit[j])+"\n")


for num_trials in all_trials:
    print("Running for %s trials" % num_trials)
    perm_indices = np.empty(shape=(num_trials, num_tasks_queue), dtype=int)
    
    for j in xrange(0,num_trials):
        perm_indices[j] = np.arange(32)

    subprocess.call(['cp task-sets/set-test.csv' ' current-simulation.csv'], shell=True)  
    subprocess.call(['./trials_simulator simple_cluster.xml deployment_cluster.xml -state > states/set-test.csv'], shell=True)

    if(os.path.exists("result-temp.dat") == True):
        subprocess.call(['rm result-temp.dat'], shell=True)

    if(os.path.exists("training-data/set-test.csv") == True):
        subprocess.call(['rm training-data/set-test.csv'], shell=True)  

    shufle_tasks_queue_runtimes = np.copy(tasks_queue_runtimes)
    shuffle_tasks_queue_nodes = np.copy(tasks_queue_nodes)
    shuffle_tasks_queue_submit = np.copy(tasks_queue_submit)

    start_time = time.time()

    for j in xrange(0,num_trials):
        with open("current-simulation.csv", "w+") as iteration_file:
            #random shuffle between the tasks in the queue
            for k in xrange(0,32):
                choose = random.randint(0,31)
                buffer_runtimes = shufle_tasks_queue_runtimes[choose]
                buffer_nodes = shuffle_tasks_queue_nodes[choose] 
                buffer_submit = shuffle_tasks_queue_submit[choose]     
                shufle_tasks_queue_runtimes[choose] = shufle_tasks_queue_runtimes[k]
                shuffle_tasks_queue_nodes[choose] = shuffle_tasks_queue_nodes[k]
                shuffle_tasks_queue_submit[choose] = shuffle_tasks_queue_submit[k]
                shufle_tasks_queue_runtimes[k] = buffer_runtimes
                shuffle_tasks_queue_nodes[k] = buffer_nodes 
                shuffle_tasks_queue_submit[k] = buffer_submit      
                buffer_index = perm_indices[j,choose]
                perm_indices[j,choose] = perm_indices[j,k]
                perm_indices[j,k] = buffer_index;
            
            for k in xrange(0,16):      
                iteration_file.write(str(tasks_state_runtimes[k])+","+str(tasks_state_nodes[k])+","+str(tasks_state_submit[k])+"\n")
            for k in xrange(0,32):   
                iteration_file.write(str(tasks_queue_runtimes[perm_indices[j,k]])+","+str(tasks_queue_nodes[perm_indices[j,k]])+","+str(tasks_queue_submit[perm_indices[j,k]])+"\n")
        
        subprocess.call(['./trials_simulator simple_cluster.xml deployment_cluster.xml >> result-temp.dat'], shell=True)
    
    print("--- %s seconds ---" % round(time.time() - start_time, 3))