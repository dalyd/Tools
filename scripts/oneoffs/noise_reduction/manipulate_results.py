#!/usr/bin/env python
'''
One off script to fix noise result data
'''

import json
import copy
import re

import itertools
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
    flat_array = list(itertools.chain(*thread_result['ops_per_sec_values']))
    thread_result['all_average'] = float(numpy.average(flat_array))
    thread_result['all_median'] = float(numpy.median(flat_array))
    thread_result['all_variance'] = float(numpy.var(flat_array, ddof=1))
    thread_result['all_variance_to_mean'] = (float(numpy.var(flat_array, ddof=1)) /
                                             float(numpy.average(flat_array)))
    thread_result['all_min'] = float(min(flat_array))
    thread_result['all_max'] = float(max(flat_array))
    thread_result['all_range'] = (float(max(flat_array)) - float(min(flat_array)))
    thread_result['all_range_to_median'] = ((float(max(flat_array)) -
                                             float(min(flat_array))) /
                                            float(numpy.median(flat_array)))

def split_results_task(task):
    ''' Split the mc results into mc and primary results for a task. Assumes 1 thread only '''

    pattern = re.compile('mc_')
    # Since we are updating with new entries, need items rather than iteritems
    for name, value in task.items():
        if pattern.match(name):
            primary_name = pattern.sub('primary_', name)
            primary_result = copy.deepcopy(value)
            primary_result['1']['ops_per_sec_values'] = [result[5:10] for result in
                                                         value['1']['ops_per_sec_values']]
            recompute_ops_per_sec(primary_result['1'])
            value['1']['ops_per_sec_values'] = [result[0:5] for result in
                                                value['1']['ops_per_sec_values']]
            recompute_ops_per_sec(value['1'])
            task[primary_name] = primary_result

def update_results():
    ''' update results '''
    results = load_data()
    for var in results.itervalues():
        for task in var.itervalues():
            split_results_task(task)

    with open('update_results.json', 'w') as output:
        json.dump(results, output, indent=4, sort_keys=True)

if __name__ == '__main__':
    update_results()
