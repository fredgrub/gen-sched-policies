#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess

tests = [
    'test_sched_perfomrance_model256_runtime.py',
    'test_sched_perfomrance_model1024_runtime.py',
    'test_sched_perfomrance_model256_estimate.py',
    'test_sched_perfomrance_model1024_estimate.py'
    'test_sched_perfomrance_model256_backfilling.py',
    'test_sched_perfomrance_model1024_backfilling.py',
    'test_sched_perfomrance_curie_runtime.py',
    'test_sched_perfomrance_anl_runtime.py',
    'test_sched_perfomrance_sdscblue_runtime.py',
    'test_sched_perfomrance_ctcsp2_runtime.py',
    'test_sched_perfomrance_hpc2n_runtime.py',
    'test_sched_perfomrance_sdscsp2_runtime.py',
    'test_sched_perfomrance_curie_estimate.py',
    'test_sched_perfomrance_anl_estimate.py',
    'test_sched_perfomrance_sdscblue_estimate.py',
    'test_sched_perfomrance_ctcsp2_estimate.py',
    'test_sched_perfomrance_hpc2n_estimate.py',
    'test_sched_perfomrance_sdscsp2_estimate.py',
    'test_sched_perfomrance_curie_backfilling.py',
    'test_sched_perfomrance_anl_backfilling.py',
    'test_sched_perfomrance_sdscblue_backfilling.py',
    'test_sched_perfomrance_ctcsp2_backfilling.py',
    'test_sched_perfomrance_hpc2n_backfilling.py',
    'test_sched_perfomrance_sdscsp2_backfilling.py'
]

logs = [
    'model256_runtime',
    'model1024_runtime',
    'model256_estimate',
    'model1024_estimate'
    'model256_backfilling',
    'model1024_backfilling',
    'curie_runtime',
    'anl_runtime',
    'sdscblue_runtime',
    'ctcsp2_runtime',
    'hpc2n_runtime',
    'sdscsp2_runtime',
    'curie_estimate',
    'anl_estimate',
    'sdscblue_estimate',
    'ctcsp2_estimate',
    'hpc2n_estimate',
    'sdscsp2_estimate',
    'curie_backfilling',
    'anl_backfilling',
    'sdscblue_backfilling',
    'ctcsp2_backfilling',
    'hpc2n_backfilling',
    'sdscsp2_backfilling'
]

for index, test in enumerate(tests):
    log_file = logs[index]
    with open('logs/' + log_file + '.log', 'w+') as log:
        subprocess.call(['python ' + test], shell=True, stdout=log)

