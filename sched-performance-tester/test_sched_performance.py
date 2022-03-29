import numpy as np
import re
import subprocess
import csv

swf_files = {
    "ANL": "swfs/ANL-Intrepid-2009-1.swf",
    "CTC": "swfs/CTC-SP2-1996-3.1-cln.swf",
    "CURIE": "swfs/CEA-Curie-2011-2.1-cln.swf",
    "C2N": "swfs/HPC2N-2002-2.2-cln.swf",
    "BLUE": "swfs/SDSC-BLUE-2000-4.2-cln.swf",
    "SP2": "swfs/SDSC-SP2-1998-4.2-cln.swf",
    "256R": "swfs/lublin_256.swf",
    "1024R": "swfs/lublin_1024.swf",
    "256E": "swfs/lublin_256_est.swf",
    "1024E": "swfs/lublin_1024_est.swf"
}

scenarios = [
    "Using actual runtimes, backfilling disabled",
    "Using processing time estimates, backfilling disabled",
    "Using processing time estimates, backfilling enabled"
    ]

configurations = {
    "ANL-B": [
        swf_files["ANL"],
        scenarios[2],
        15,
        False,
        "./sched-simulator-estimate-backfilling xmls/plat_day.xml xmls/deployment_anl.xml -nt -bf "
        ],
    "ANL-E": [
        swf_files["ANL"],
        scenarios[1],
        15,
        False,
        "./sched-simulator-estimate-backfilling xmls/plat_day.xml xmls/deployment_anl.xml -nt "
        ],
    "ANL-R": [
        swf_files["ANL"],
        scenarios[0],
        15,
        True,
        "./sched-simulator-runtime xmls/plat_day.xml xmls/deployment_anl.xml -nt ",
        ],
    "CTC-B": [
        swf_files["CTC"],
        scenarios[2],
        22,
        False,
        "./sched-simulator-estimate-backfilling xmls/plat_day.xml xmls/deployment_ctcsp2.xml -nt -bf ",
        ],
    "CTC-E": [
        swf_files["CTC"],
        scenarios[1],
        22,
        False,
        "./sched-simulator-estimate-backfilling xmls/plat_day.xml xmls/deployment_ctcsp2.xml -nt ",
        ],
    "CTC-R": [
        swf_files["CTC"],
        scenarios[0],
        22,
        True,
        "./sched-simulator-runtime xmls/plat_day.xml xmls/deployment_ctcsp2.xml -nt ",
        ],
    "CURIE-B": [
        swf_files["CURIE"],
        scenarios[2],
        15,
        False,
        "./sched-simulator-estimate-backfilling xmls/plat_day.xml xmls/deployment_curie.xml -nt -bf ",
        ],
    "CURIE-E": [
        swf_files["CURIE"],
        scenarios[1],
        15,
        False,
        "./sched-simulator-estimate-backfilling xmls/plat_day.xml xmls/deployment_curie.xml -nt ",
        ],
    "CURIE-R": [
        swf_files["CURIE"],
        scenarios[0],
        15,
        True,
        "./sched-simulator-runtime xmls/plat_day.xml xmls/deployment_curie.xml -nt ",
        ],
    "C2N-B": [
        swf_files["C2N"],
        scenarios[2],
        83,
        False,
        "./sched-simulator-estimate-backfilling xmls/plat_day.xml xmls/deployment_hpc2n.xml -nt -bf ",
        ],
    "C2N-E": [
        swf_files["C2N"],
        scenarios[1],
        83,
        False,
        "./sched-simulator-estimate-backfilling xmls/plat_day.xml xmls/deployment_hpc2n.xml -nt ",
        ],
    "C2N-R": [
        swf_files["C2N"],
        scenarios[0],
        83,
        True,
        "./sched-simulator-runtime xmls/plat_day.xml xmls/deployment_hpc2n.xml -nt ",
        ],
    "BLUE-B": [
        swf_files["BLUE"],
        scenarios[2],
        64,
        False,
        "./sched-simulator-estimate-backfilling xmls/plat_day.xml xmls/deployment_blue.xml -nt -bf ",
        ],
    "BLUE-E": [
        swf_files["BLUE"],
        scenarios[1],
        64,
        False,
        "./sched-simulator-estimate-backfilling xmls/plat_day.xml xmls/deployment_blue.xml -nt ",
        ],
    "BLUE-R": [
        swf_files["BLUE"],
        scenarios[0],
        64,
        True,
        "./sched-simulator-runtime xmls/plat_day.xml xmls/deployment_blue.xml -nt ",
        ],
    "SP2-B": [
        swf_files["SP2"],
        scenarios[2],
        47,
        False,
        "./sched-simulator-estimate-backfilling xmls/plat_day.xml xmls/deployment_sdscsp2.xml -nt -bf ",
        ],
    "SP2-E": [
        swf_files["SP2"],
        scenarios[1],
        47,
        False,
        "./sched-simulator-estimate-backfilling xmls/plat_day.xml xmls/deployment_sdscsp2.xml -nt ",
        ],
    "SP2-R": [
        swf_files["SP2"],
        scenarios[0],
        47,
        True,
        "./sched-simulator-runtime xmls/plat_day.xml xmls/deployment_sdscsp2.xml -nt ",
        ],
    "256-B": [
        swf_files["256E"],
        scenarios[2],
        50,
        False,
        "./sched-simulator-estimate-backfilling xmls/plat_day.xml xmls/deployment_day.xml -nt -bf ",
        ],
    "256-E": [
        swf_files["256E"],
        scenarios[1],
        50,
        False,
        "./sched-simulator-estimate-backfilling xmls/plat_day.xml xmls/deployment_day.xml -nt ",
        ],
    "256-R": [
        swf_files["256R"],
        scenarios[0],
        50,
        True,
        "./sched-simulator-runtime xmls/plat_day.xml xmls/deployment_day.xml -nt ",
        ],
    "1024-B": [
        swf_files["1024E"],
        scenarios[2],
        50,
        False,
        "./sched-simulator-estimate-backfilling xmls/plat_day.xml xmls/deployment_day_1024.xml -nt -bf ",
        ],
    "1024-E": [
        swf_files["1024E"],
        scenarios[1],
        50,
        False,
        "./sched-simulator-estimate-backfilling xmls/plat_day.xml xmls/deployment_day_1024.xml -nt ",
        ],
    "1024-R": [
        swf_files["1024R"],
        scenarios[0],
        50,
        True,
        "./sched-simulator-runtime xmls/plat_day.xml xmls/deployment_day_1024.xml -nt ",
        ]
}

policies = {
    "FCFS": '',
    "SJF": '-spt',
    "WFP3": '-wfp3',
    "UNICEF": '-unicef',
    "F1": '-f1',
    "F2": '-f2',
    "F3": '-f3',
    "F4": '-f4',
    "LIN": '-linear',
    "SQ": '-quadratic',
    "CUB": '-cubic',
    "QUA": '-quartic',
    "SAF": '-saf'
}

exec_policies = ["FCFS", "WFP3", "UNICEF", "SJF", "SAF", "F2", "LIN"]

SECONDS_IN_A_DAY = 86400
SIM_NUM_DAYS = 15

NUM_TASKS_QUEUE = 32
NUM_TASKS_STATE = 16

def execute_tests(config, specs):
    swf_file = specs[0]
    scenario = specs[1]
    num_experiments = specs[2]
    use_actual = specs[3]
    exec_code = specs[4]

    model_run_times = []
    model_req_run_times = []
    model_num_nodes = []
    model_submit_times = []

    with open(swf_file) as f:
        for line in f:
            row = re.split(" +", line.lstrip(" "))
            if row[0].startswith(";"):
                continue  
            if int(row[4]) > 0 and int(row[3]) > 0 and int(row[8]) > 0:
                model_run_times.append(int(row[3]))
                model_req_run_times.append(int(row[8]))
                model_num_nodes.append(int(row[4]))
                model_submit_times.append(int(row[1]))

    timespan = np.max(model_submit_times) - np.min(model_submit_times)

    print('Performing scheduling performance test for the workload trace %s\n' % swf_file +
     'Configuration: %s' % scenario)

    slowdown_csv = open('slowdowns/' + config + '.csv', 'a')
    write = csv.writer(slowdown_csv)
    write.writerow(exec_policies)

    choose = 0
    for i in range(0,num_experiments): #1e7  
        task_file = open("initial-simulation-submit.csv", "w+")
        tasks_state_nodes = []
        tasks_state_runtimes = []
        tasks_state_req_runtimes = []
        tasks_state_submit = []

        earliest_submit = model_submit_times[choose]
        
        for j in range(0,16):
            tasks_state_nodes.append(model_num_nodes[choose+j])
            tasks_state_runtimes.append(model_run_times[choose+j])
            tasks_state_req_runtimes.append(model_req_run_times[choose+j])
            tasks_state_submit.append(model_submit_times[choose+j] - earliest_submit)
            if use_actual:
                task_file.write(str(tasks_state_runtimes[j])+","+str(tasks_state_nodes[j])+","+str(tasks_state_submit[j])+"\n")
            else:
                task_file.write(str(tasks_state_runtimes[j])+","+str(tasks_state_nodes[j])+","+str(tasks_state_submit[j])+str(tasks_state_req_runtimes)+"\n")
        tasks_queue_nodes = []
        tasks_queue_runtimes = []
        tasks_queue_req_runtimes = []
        tasks_queue_submit = []
        
        j = 0
        while model_submit_times[choose+NUM_TASKS_STATE+j] - earliest_submit <= SECONDS_IN_A_DAY * SIM_NUM_DAYS:
            tasks_queue_nodes.append(model_num_nodes[NUM_TASKS_STATE+choose+j])
            tasks_queue_runtimes.append(model_run_times[NUM_TASKS_STATE+choose+j])
            tasks_queue_req_runtimes.append(model_req_run_times[NUM_TASKS_STATE+choose+j])
            tasks_queue_submit.append(model_submit_times[NUM_TASKS_STATE+choose+j] - earliest_submit)
            if use_actual:
                task_file.write(str(tasks_queue_runtimes[j])+","+str(tasks_queue_nodes[j])+","+str(tasks_queue_submit[j])+"\n")
            else:
                task_file.write(str(tasks_queue_runtimes[j])+","+str(tasks_queue_nodes[j])+","+str(tasks_queue_submit[j])+str(tasks_queue_req_runtimes)+"\n")
            j=j+1
        task_file.close()
        choose = choose + NUM_TASKS_STATE + j

        number_of_tasks = len(tasks_queue_runtimes) + len(tasks_state_runtimes) 
        print('Performing scheduling experiment %d. Number of tasks=%d' % (i+1, number_of_tasks))

        _buffer = open("plot-temp.dat", "w+")
        for policy in exec_policies:
            pflag = policies[policy]
            subprocess.call([exec_code + pflag + " " + str(number_of_tasks)], shell=True, stdout=_buffer)
        _buffer.close()
        
        _buffer = open("plot-temp.dat", "r")
        lines = list(_buffer)
        write.writerow(lines)
        _buffer.close()

for config, specs in configurations.items():
    execute_tests(config, specs)