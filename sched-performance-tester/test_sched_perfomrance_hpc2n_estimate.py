#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import numpy as np
import re
import random
import subprocess

import matplotlib as mpl
mpl.use('Agg')

import matplotlib.pyplot as plt

# Iterate over the rows, splitting the label from the features. Convert labels
# to integers and features to floats.
#filename = "lublin_256_20k.swf"
#filename = "CEA-Curie-2011-2.1-cln.swf"
#filename = "METACENTRUM-2013-3.swf"
filename = "swfs/HPC2N-2002-2.2-cln.swf"
#filename = "SDSC-SP2-1998-4.2-cln.swf"
#filename = "CTC-SP2-1996-3.1-cln.swf"

model_num_nodes = []
model_run_times = []
model_req_run_times = []
model_submit_times = []
num_tasks_queue = 32
num_tasks_state = 16
earliest_submit = 0
tasks_state_nodes = []
tasks_state_runtimes = []
tasks_state_submit = []
tasks_state_req_runtimes = []
tasks_queue_nodes = []
tasks_queue_runtimes = []
tasks_queue_req_runtimes = []
tasks_queue_submit = []
SECONDS_IN_A_DAY = 86400

SIM_NUM_DAYS = 15
NUM_EXPERIMENTS = 83

slow_sjf = []
slow_fcfs = []
slow_wfp3 = []
slow_unicef = []
slow_c1 = []
slow_c2 = []
slow_c3 = []
slow_c4 = []
slow_c5 = []
slow_c6 = []
slow_nn = []

for line in file(filename):
  row = re.split(" +", line.lstrip(" "))
  if row[0].startswith(";"):    
    continue
  #print("%f %d" % (float(row[4]), int(row[5])))  
  if int(row[4]) > 0 and int(row[3]) > 0 and int(row[8]) > 0:
    model_run_times.append(int(row[3]))
    model_req_run_times.append(int(row[8]))
    model_num_nodes.append(int(row[4]))
    model_submit_times.append(int(row[1]))

timespan = np.max(model_submit_times) - np.min(model_submit_times) 

#random.seed(None)

choose = 0
for i in xrange(0,NUM_EXPERIMENTS): #1e7  
  task_file = open("initial-simulation-submit.csv", "w+")
  tasks_state_nodes = []
  tasks_state_runtimes = []
  tasks_state_req_runtimes = []
  tasks_state_submit = []
  #choose = random.randint(0,len(model_run_times)-1 - (num_tasks_queue+num_tasks_state))
  earliest_submit = model_submit_times[choose]
  for j in xrange(0,16):
    tasks_state_nodes.append(model_num_nodes[choose+j])
    tasks_state_runtimes.append(model_run_times[choose+j])
    tasks_state_req_runtimes.append(model_req_run_times[choose+j])
    tasks_state_submit.append(model_submit_times[choose+j] - earliest_submit)
    task_file.write(str(tasks_state_runtimes[j])+","+str(tasks_state_nodes[j])+","+str(tasks_state_submit[j])+","+str(tasks_state_req_runtimes[j])+"\n")
  tasks_queue_nodes = []
  tasks_queue_runtimes = []
  tasks_queue_req_runtimes = []
  tasks_queue_submit = []
  j = 0
  while model_submit_times[choose+num_tasks_state+j] - earliest_submit <= SECONDS_IN_A_DAY * SIM_NUM_DAYS:
    #choose = random.randint(0,len(model_run_times)-1)
    tasks_queue_nodes.append(model_num_nodes[num_tasks_state+choose+j])
    tasks_queue_runtimes.append(model_run_times[num_tasks_state+choose+j])
    tasks_queue_req_runtimes.append(model_req_run_times[num_tasks_state+choose+j])
    tasks_queue_submit.append(model_submit_times[num_tasks_state+choose+j] - earliest_submit)
    task_file.write(str(tasks_queue_runtimes[j])+","+str(tasks_queue_nodes[j])+","+str(tasks_queue_submit[j])+","+str(tasks_queue_req_runtimes[j])+"\n")
    j=j+1
  task_file.close()
  choose = choose + num_tasks_state + j

  number_of_tasks = len(tasks_queue_runtimes) + len(tasks_state_runtimes) 
  print("%d %d" % (i,number_of_tasks))  

 
  _buffer = open("plot-temp.dat", "w+")
  subprocess.call(['./sched-simulator-estimate-backfilling xmls/plat_day.xml xmls/deployment_hpc2n.xml -nt '+str(number_of_tasks)], shell=True, stdout=_buffer)
  subprocess.call(['./sched-simulator-estimate-backfilling xmls/plat_day.xml xmls/deployment_hpc2n.xml -wfp3 -nt '+str(number_of_tasks)], shell=True, stdout=_buffer)
  subprocess.call(['./sched-simulator-estimate-backfilling xmls/plat_day.xml xmls/deployment_hpc2n.xml -unicef -nt '+str(number_of_tasks)], shell=True, stdout=_buffer)
  subprocess.call(['./sched-simulator-estimate-backfilling xmls/plat_day.xml xmls/deployment_hpc2n.xml -spt -nt '+str(number_of_tasks)], shell=True, stdout=_buffer)  
  #subprocess.call(['./heuristics_simulator_submittime_day_estimates xmls/plat_day.xml xmls/deployment_blue.xml -c1 -nt '+str(number_of_tasks)], shell=True, stdout=_buffer)
  #subprocess.call(['./heuristics_simulator_submittime_day_estimates xmls/plat_day.xml xmls/deployment_blue.xml -c2 -nt '+str(number_of_tasks)], shell=True, stdout=_buffer)
  # subprocess.call(['./sched-simulator-estimate-backfilling xmls/plat_day.xml xmls/deployment_hpc2n.xml -f4 -nt '+str(number_of_tasks)], shell=True, stdout=_buffer)
  # subprocess.call(['./sched-simulator-estimate-backfilling xmls/plat_day.xml xmls/deployment_hpc2n.xml -f3 -nt '+str(number_of_tasks)], shell=True, stdout=_buffer)
  subprocess.call(['./sched-simulator-estimate-backfilling xmls/plat_day.xml xmls/deployment_hpc2n.xml -saf -nt '+str(number_of_tasks)], shell=True, stdout=_buffer)
  subprocess.call(['./sched-simulator-estimate-backfilling xmls/plat_day.xml xmls/deployment_hpc2n.xml -f2 -nt '+str(number_of_tasks)], shell=True, stdout=_buffer)
  subprocess.call(['./sched-simulator-estimate-backfilling xmls/plat_day.xml xmls/deployment_hpc2n.xml -linear -nt '+str(number_of_tasks)], shell=True, stdout=_buffer)
  #subprocess.call(['./nn_simulator simple_cluster.xml deployment_cluster.xml'], shell=True, stdout=_buffer)
  _buffer.close()

  _buffer = open("plot-temp.dat", "r")
  lines = list(_buffer)  
  slow_fcfs.append(float(lines[0]))
  slow_wfp3.append(float(lines[1]))
  slow_unicef.append(float(lines[2]))
  slow_sjf.append(float(lines[3]))
  #slow_easy.append(float(lines[3]))
  #slow_nn.append(float(lines[4]))
  #slow_c1.append(float(lines[4]))
  #slow_c2.append(float(lines[5]))
  slow_c3.append(float(lines[4]))
  slow_c4.append(float(lines[5]))
  slow_c5.append(float(lines[6]))
  # slow_c6.append(float(lines[7]))
  _buffer.close()
  

#people = ('FCFS', 'LPT', 'WFP3', 'UNICEF', 'NN')
#people = ('FCFS', 'SJF', 'WFP3', 'UNICEF', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6')
#people = ('EASY', 'WFP3', 'UNICEF', 'F1', 'F2')
people = ('FCFS', 'WFP3', 'UNICEF', 'SJF', 'SAF', 'F2', 'Lin')
y_pos = np.arange(len(people))

performance = []
performance.append(np.mean(slow_fcfs))
performance.append(np.mean(slow_wfp3))
performance.append(np.mean(slow_unicef))
performance.append(np.mean(slow_sjf))
#performance.append(np.mean(slow_easy))
#performance.append(np.mean(slow_nn))
#performance.append(np.mean(slow_c1))
#performance.append(np.mean(slow_c2))
performance.append(np.mean(slow_c3))
performance.append(np.mean(slow_c4))
performance.append(np.mean(slow_c5))
# performance.append(np.mean(slow_c6))

error = []
error.append(np.std(slow_fcfs))
error.append(np.std(slow_wfp3))
error.append(np.std(slow_unicef))
error.append(np.std(slow_sjf))
#error.append(np.std(slow_easy))
#error.append(np.std(slow_nn))
#error.append(np.std(slow_c1))
#error.append(np.std(slow_c2))
error.append(np.std(slow_c3))
error.append(np.std(slow_c4))
error.append(np.std(slow_c5))
# error.append(np.std(slow_c6))


#plt.rc("font", size=30)
#plt.figure(figsize=(16,14))
#plt.bar(y_pos, performance, yerr=None, align='center', alpha=1.0, color='c')
#plt.xticks(y_pos, people)
#plt.xlabel(u'Scheduling Policies')
#plt.ylabel('Average Bounded Slowdown')
#plt.ylim(0,7000)
#plt.title('Workload Model')

#for i in range(0,len(performance)):
#  plt.text(y_pos[i],performance[i],"%.2f" % (round(performance[i], 1)), horizontalalignment='center', #verticalalignment='bottom', color='black')
#  plt.text(y_pos[i],performance[i],"%.1f\n%.1f" % (round(performance[i], 1),round(error[i], 1)), horizontalalignment='center', verticalalignment='bottom', color='black')
  #plt.text(y_pos[i],performance[i]+1,str(round(error[i], 4)), horizontalalignment='center', color='red')

#plt.show()
#plt.savefig('plots/CLUSTER/model_256_r_nbf.eps', format='eps', dpi=1000)

#results_file = open("results/blue_bf.csv","w+")
#for i in range(0,len(performance)):
#  if i == len(performance)-1:
#    results_file.write(str(performance[i])+"\n")
#  else:
#    results_file.write(str(performance[i])+",")

#for i in range(0,len(error)):
#  if i == len(error)-1:
#    results_file.write(str(error[i])+"\n")
#  else:
#    results_file.write(str(error[i])+",")
#results_file.close()

#fig, axes = plt.subplots(nrows=1, ncols=1)

# arrange data
all_data = []

all_data.append(slow_fcfs)
all_data.append(slow_wfp3)
all_data.append(slow_unicef)
all_data.append(slow_sjf)
all_data.append(slow_c3)
all_data.append(slow_c4)
all_data.append(slow_c5)
# all_data.append(slow_c6)

plt.rc("font", size=45)
plt.figure(figsize=(16,14))

all_medians = []

axes = plt.axes()

new_all_data = np.array(all_data)

OUT_POLICIES = 7
MAX_OUT = [0,0,0,0,0,0,0]

OUT_CUT = 9

outliers = np.zeros((OUT_POLICIES,max(MAX_OUT)))

xticks=[y+1 for y in range(len(all_data))]

for i in range(0,OUT_POLICIES):
  temp = new_all_data[i,:]      
  plt.plot(xticks[i], np.reshape(temp, (1,len(temp))), 'o', color='darkorange')
  #plt.boxplot(temp, showfliers=False)

for i in range(0,OUT_POLICIES):
  temp = new_all_data[i,:]
  for j in range(0,MAX_OUT[i]):
    _max = np.max(temp)
    outliers[i,j] = _max
    temp = np.delete(temp,np.argmax(temp)) 

#print(new_all_data)
# plt.plot(xticks[0:1], new_all_data[0:1], 'o', color='darkorange')
# plt.plot(xticks[1:2], new_all_data[1:2], 'o', color='darkorange')
# plt.plot(xticks[2:3], new_all_data[2:3], 'o', color='darkorange')
# plt.plot(xticks[3:4], new_all_data[3:4], 'o', color='darkorange')
# plt.plot(xticks[4:5], new_all_data[4:5], 'o', color='darkorange')
# plt.plot(xticks[5:6], new_all_data[5:6], 'o', color='darkorange')
# plt.plot(xticks[6:7], new_all_data[6:7], 'o', color='darkorange')
#plt.plot(xticks[7:8], new_all_data[7:8], 'o', color='darkorange')

plt.ylim((0,600))

xoffset=[0.32,0.32,0.32,0.32,0.32,0.32,0.32]
ylow=[550,550,550,550,550,550,550]

for i in range(0,OUT_POLICIES):
  output = ''
  if MAX_OUT[i] != 0:
    for j in range(0,MAX_OUT[i]):
      if j == MAX_OUT[i] - 1:
        output = output+'%.1f' % (outliers[i,j])
      else:
        output = output+'%.1f' % (outliers[i,j])+'\n'
  #  continue
  #output=''
  #if i == 3 or i == 1:
  #  output = '%.1f' % (outliers[i,0])  
    plt.annotate(output, xy=(xticks[i], 600), xytext=(xticks[i]-xoffset[i], ylow[i]),
            arrowprops=dict(facecolor='black', shrink=0.05),fontsize=25)

for p in all_data:
  all_medians.append(np.median(p))

# plot box plot
plt.boxplot(all_data, showfliers=False)
#axes[1].set_title('box plot')

# adding horizontal grid lines
#for ax in axes:
axes.yaxis.grid(True)
axes.set_xticks([y+1 for y in range(len(all_data))])
#axes.set_xlabel('Scheduling Policies', fontsize=45)
#axes.set_ylabel('Average Bounded Slowdown',  fontsize=45)

# add x-tick labels
xticklabels=['FCFS', 'WFP', 'UNI', 'SPT', 'SAF', 'F2', 'Lin']
plt.setp(axes, xticks=[y+1 for y in range(len(all_data))], xticklabels=['FCFS', 'WFP', 'UNI', 'SPT', 'SAF', 'F2', 'Lin'])

plt.tick_params(axis='both', which='major', labelsize=45)
plt.tick_params(axis='both', which='minor', labelsize=45)

#plt.show()
plt.savefig('plots/hpc2n_e_nbf.pdf', format='pdf', dpi=1000,bbox_inches='tight')

print('Experiment Statistics:')
print('Medians:')
i=0
for m in all_medians:
  print('%s=%.2f' % (xticklabels[i],m))
  i=i+1
print('Means:')
i=0
for p in performance:
  print('%s=%.2f' % (xticklabels[i],p))
  i=i+1
print('Standard Deviations:')
i=0
for e in error:
  print('%s=%.2f' % (xticklabels[i],e))
  i=i+1

print('Boxplot saved in file hpc2n_e_nbf.pdf')




#print("%d" % random.randint(2,8))
  
