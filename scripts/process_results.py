#!/usr/bin/env python

import pymongo
import math
import subprocess
import numpy
import json
import glob

client = pymongo.MongoClient()


def per_test_data(results) : 
    ''' Process results to print out per test data. Assumes 7 iterations for now.  '''
    out = open("results.csv", "w")
    out.write('name,threads,median,averages,stddev,n,stddev/avg,range/avg,githash,endtime,x1,x2,x3,x4,x5,x6,x7\n')
    for r in results : 
        for res in r['data']['results'] : 
                for key in res['results'] :
                    if key.isnumeric(): 
                        values = res['results'][key]['ops_per_sec_values']
                        median = numpy.median(values)
                        stddev = numpy.std(values)
                        ranged = max(values) - min(values)
                        valstring = ','.join(str(val) for val in values)
                        out.write(res['name']+','+ key+','+ str(median) +','+ str(res['results'][key]["ops_per_sec"])+','+ str(stddev)+',' + str(len(values)) + ',' + str(stddev/res['results'][key]['ops_per_sec']) + ',' + str(ranged/res['results'][key]['ops_per_sec']) + ',' + r['revision'] +','+ r['data']['end'] + ',' + valstring +  '\n')

def per_iteration_data(results) : 
    ''' Process results to print out data per test iteration. Removes mongo-perfs default aggregation  '''
    out = open("results.iter.csv", "w")
    out.write('name,threads,median,averages,stddev,n,x,githash,endtime\n')
    for r in results : 
        for res in r['data']['results'] : 
                for key in res['results'] :
                    if key.isnumeric(): 
                        values = res['results'][key]['ops_per_sec_values']
                        median = numpy.median(values)
                        stddev = numpy.std(values)
                        for val in values : 
                            out.write(res['name']+','+ key+','+ str(median) +','+ str(res['results'][key]["ops_per_sec"])+','+ str(stddev)+',' + str(len(values)) + ',' +str(val)+ ',' + r['revision'] +','+ r['data']['end']+ '\n')

def load_data(filename='results.json') : 
    ''' Read the input file into a json array '''
    results = json.load(open(filename))
    # Check if it is a list. If it isn't, put it in a list
    if isinstance(results, list) : 
        return results
    else :
        return [results]

def load_all_data() :
    ''' Load all the json files in the directory '''
    results = []
    for file in glob.glob("*.json") : 
        results.extend(load_data(file))
    return results

def import_data(filename='results.json', dbname='results', colname='test') : 
    ''' Import json from filename

    This is going to import the data into mongod, for later query. The main benefit of this is handling the extended json '''
    
    # import the data. Dropp the collection first. 
    subprocess.call(['mongoimport',  '-d', dbname, '-c', colname, filename, '--drop', '--jsonArray'])
    

if __name__ == "__main__":
    
    results = load_all_data()
    per_test_data(results)
    per_iteration_data(results)
