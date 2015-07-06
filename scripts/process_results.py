#!/usr/bin/env python

import pymongo
import math
import subprocess

client = pymongo.MongoClient()

def per_test_data(results) : 
    ''' Process results to print out per test data. Assumes 7 iterations for now.  '''
    out = open("results.csv", "w")
    out.write('name,threads,median,averages,stddev,n,invstddev,time,stddev/avg,x1,x2,x3,x4,x5,x6,x7\n')
    for r in results : 
        if 'singledb' in r : 
            for res in r['singledb'] : 
                for key in res['nresults'] : 
                    if key.isdigit(): 
                        values = res['nresults'][key]['ops_per_sec_values']
                        inv_values = [ 1/val for val in values ] 
                        inv_mean = sum(inv_values)/len(inv_values)
                        inv_secmom = sum((x*x for x in inv_values))
                        inv_stddev = math.sqrt(inv_secmom - inv_mean*inv_mean)
                        valstring = ','.join(str(val) for val in values)
                        out.write(res['name']+','+ key+','+ str(res['nresults'][key]['median']) +','+ str(res['nresults'][key]["ops_per_sec"])+','+ str(res['nresults'][key]['standardDeviation'])+','+ str(res['nresults'][key]['n'])+','+str(inv_stddev) + ',' + str(res['nresults'][key]['elapsed_secs'])+','+ str(res['nresults'][key]['standardDeviation']/res['nresults'][key]['ops_per_sec']) + ',' + valstring + '\n')

def per_iteration_data(results) : 
    ''' Process results to print out data per test iteration. Removes mongo-perfs default aggregation  '''
    out = open("results.iter.csv", "w")
    out.write('name,threads,median,averages,stddev,x,n,time\n')
    for r in results : 
        if 'singledb' in r : 
            for res in r['singledb'] : 
                for key in res['nresults'] : 
                    if key.isdigit() : 
                        values = res['nresults'][key]['ops_per_sec_values']
                        for val in values : 
                            out.write(res['name']+','+ key+','+ str(res['nresults'][key]['median']) +','+ str(res['nresults'][key]["ops_per_sec"])+','+ str(res['nresults'][key]['standardDeviation'])+','+ str(res['nresults'][key]['n'])+','+str(val) + ',' + str(res['nresults'][key]['elapsed_secs'])+'\n')

def import_data(filename='results.json', dbname='results', colname='test') : 
    ''' Import json from filename

    This is going to import the data into mongod, for later query. The main benefit of this is handling the extended json '''
    
    # import the data. Dropp the collection first. 
    subprocess.call(['mongoimport',  '-d', dbname, '-c', colname, filename, '--drop', '--jsonArray'])
    

if __name__ == "__main__":
    import_data()
    coll = client.results['test']
    results = coll.find()
    per_test_data(results)
    results = coll.find()
    per_iteration_data(results)
