#!/usr/bin/env python
'''
Script to generate graphs
'''

from __future__ import print_function

import numpy
import pymongo

def add_it_stats(collection):
    '''
    Add max, min, and average stats for the it_range_to_median array
    '''
    for doc in collection.find():
        doc['it_range_to_median_avg'] = numpy.average(doc['it_range_to_median'])
        doc['it_range_to_median_max'] = max(doc['it_range_to_median'])
        doc['it_range_to_median_min'] = min(doc['it_range_to_median'])
        collection.update({'_id': doc['_id']}, doc)


def real_io_test_name(test_name, rw):
    ''' Generate test name'''
    if test_name == 'latency':
        return 'primary_{}_test_{}_clat_mean'.format(test_name, rw)
    else:
        return 'primary_{}_test_{}_iops'.format(test_name, rw)

def real_benchrun_test_name(test_name, storage_engine):
    '''Make test names
    '''
    return '{}-{}'.format(test_name, storage_engine)

def average_across_cursor(curr):
    '''Generate averages across a cursor'''
    entries = [doc for doc in curr]
    averaged_results = {}
    for key in entries[0]:
        averaged_results[key] = numpy.average([doc[key] for doc in entries])
    return averaged_results

def generate_io_summary(collection):
    ''' Generate CSV summary of IO tests '''
    qfilter = {'_id': 0, 'range_to_median': 1, 'all_range_to_median': 1, 'it_range_to_median_avg':1,
               'it_range_to_median_max':1}
    base_tests = ['latency', 'iops_', 'streaming_bandwidth']
    base_tests = ['latency', 'iops', 'streaming_bandwidth']
    print('test name,R/W,range to median,all range to median,per task range to median avg,'
          'per task range to median max')
    for test in base_tests:
        for rw in ['read', 'write']:
            curr = collection.find({'test_name': real_io_test_name(test, rw)}, qfilter)
            results = average_across_cursor(curr)
            print('{},{},{},{},{},{}'.format(test.strip('_'), rw, results['range_to_median'],
                                             results['all_range_to_median'],
                                             results['it_range_to_median_avg'],
                                             results['it_range_to_median_max']))

# Can modify to include thread info
def generate_benchrun_summary(collection):
    ''' Generate CSV summary of benchrun tests '''
    qfilter = {'_id': 0, 'range_to_median': 1, 'all_range_to_median': 1, 'it_range_to_median_avg':1,
               'it_range_to_median_max':1}
    benchrun_tests = ['contended_update',
                      'index_build',
                      'initial_load_capped',
                      'insert_capped',
                      'insert_capped_indexes',
                      'insert_jtrue',
                      'insert_ttl',
                      'insert_vector_primary',
                      'map_reduce_1M_doc',
                      'removemulti_jtrue',
                      'updatemulti_jtrue',
                      'word_count_1M_doc']
    print('test name,SE,range to median,all range to median,per task range to median avg,'
          'per task range to median max')
    for se in ['wiredTiger', 'mmapv1']:
        for test in benchrun_tests:
            curr = collection.find({'test_name': real_benchrun_test_name(test, se)}, qfilter)
            results = average_across_cursor(curr)
            print('{},{},{},{},{},{}'.format(test.strip('_'), se, results['range_to_median'],
                                             results['all_range_to_median'],
                                             results['it_range_to_median_avg'],
                                             results['it_range_to_median_max']))

def name_and_storage_engine(testname):
    '''Cleanup names and split into storage engine and test name

    The storage engine, if it exists, is the last item after a -. In
    some cases it doesn't exist. Need to handle that also. It looks
    like that's only for the fio tests, which do not have a -.

    '''
    storage_engine = ""
    parts = testname.split('-')
    if len(parts) > 1:
        testname = '_'.join(parts[:-1])
        storage_engine = parts[-1]
    return testname, storage_engine

def generate_all(collection):
    ''' Generate a dump of the whole collection, with storage engine split out '''
    curr = collection.find({})
    output = ['original test name,range to median,all range to median,per task range to median avg,'
              'per task range to median max,per task range to median min,task name,thread_level,'
              'test name,STORAGE_ENGINE']
    for doc in curr:
        testname, storage_engine = name_and_storage_engine(doc['test_name'])
        output.append(','.join([doc['test_name'], str(doc['range_to_median']),
                                str(doc['all_range_to_median']),
                                str(doc['it_range_to_median_avg']),
                                str(doc['it_range_to_median_max']),
                                str(doc['it_range_to_median_min']),
                                str(doc['task_name']),
                                str(doc['thread_level']),
                                testname, storage_engine]))
    return output

def dump_to_file(filename, collection):
    ''' Call generate all and dump to the fiven file'''
    with open(filename, 'w') as outfile:
        outfile.write('\n'.join(generate_all(collection)))

def connect():
    '''
    Connect to localhost
    '''
    client = pymongo.MongoClient()
    return client.noise

#db.baseline.count({'test_name': {'$regex' : '^(?!mc)(?!primary)'}})
