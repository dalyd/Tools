#!/usr/bin/env python

import json
import copy
import numpy


def load_data(filename='agg_results.json'):
    ''' Loads in result data'''
    with open(filename) as input_file:
        results = json.load(input_file)
    return results

def recompute_ops_per_sec(thread_result):
    ''' Compute ops_per_sec from ops_per_sec_values '''
    thread_result['ops_per_sec'] = [numpy.average(values) for values in
                                    thread_result['ops_per_sec_values']]
    val = thread_result['ops_per_sec']
    thread_result['average'] = float(numpy.average(val))
    thread_result['median'] = float(numpy.median(val))
    thread_result['variance'] = float(numpy.var(val, ddof=1))
    thread_result['variance_to_mean'] = (float(thread_result['variance']) /
                                         float(thread_result['average']))
    thread_result['min'] = min(val)
    thread_result['max'] = max(val)
    thread_result['range'] = thread_result['max'] - thread_result['min']
    thread_result['range_to_median'] = (float(thread_result['range']) /
                                        float(thread_result['median']))
    thread_result['it_average'] = [float(numpy.average(it_results)) for it_results in
                                   thread_result['ops_per_sec_values']]
    thread_result['it_median'] = [float(numpy.median(it_results)) for it_results in
                                  thread_result['ops_per_sec_values']]
    thread_result['it_variance'] = [float(numpy.var(it_results, ddof=1)) for it_results in
                                    thread_result['ops_per_sec_values']]
    thread_result['it_variance_to_mean'] = [float(numpy.var(it_results, ddof=1)) /
                                            float(numpy.average(it_results)) for it_results in
                                            thread_result['ops_per_sec_values']]
    thread_result['it_min'] = [float(min(it_results)) for it_results in
                               thread_result['ops_per_sec_values']]
    thread_result['it_max'] = [float(numpy.max(it_results)) for it_results in
                               thread_result['ops_per_sec_values']]
    thread_result['it_range'] = [float(max(it_results)) - float(min(it_results)) for it_results in
                                 thread_result['ops_per_sec_values']]
    thread_result['it_range_to_median'] = [(float(max(it_results)) - float(min(it_results))) /
                                           float(numpy.median(it_results)) for it_results in
                                           thread_result['ops_per_sec_values']]

def split_results_task(task):
    ''' Split the mc results into mc and primary results for a task. Assumes 1 thread only '''
    for name, value in task.iteritems():
        if pattern.match(name):
            primary_name = pattern.sub('primary_', name)
            primary_result = copy.deepcopy(value)
            primary_test['1']['ops_per_sec_values'] = [result[5:10] for result in
                                                       value['1']['ops_per_sec_values']]
            recompute_ops_per_sec(primary_test['1'])
            value['1']['ops_per_sec_values'] = [result[0:5] for result in
                                                value['1']['ops_per_sec_values']]
            recompute_ops_per_sec(value['1'])
            task[primary_name] = primary_result


var = results['linux-1-node-replSet']
test = var['core_workloads_WT']['mc_latency_test_read_clat_stddev']
mc_values = [result[0:5] for result in test['1']['ops_per_sec_values']]
primary_values = [result[5:10] for result in test['1']['ops_per_sec_values']]

primary_test = copy.deepcopy(test)
primary_test['1']['ops_per_sec_values'] = [result[5:10] for result in test['1']['ops_per_sec_values']]
recompute_ops_per_sec(primary_test['1'])
test['1']['ops_per_sec_values'] = [result[0:5] for result in test['1']['ops_per_sec_values']]
recompute_ops_per_sec(test['1'])

pattern = re.compile('mc_')
fio_test_names = [filename for filename in var['core_workloads_WT'] if pattern.match(filename)]
primary_test_names = [pattern.sub('primary', filename) for filename in var['core_workloads_WT'] if pattern.match(filename)]

task = var['core_workloads_WT']
