'''
This was a one-off script to parse a collection of 1000
result.json files from running speedtest.yml. It generates a csv file
for importing into Excel

'''


import json

def ensureFields(r, fields): 
    ''' Make sure all the fields exist in M. Insert 0 if not '''
    r.update((missing, 0) for missing in set(fields).difference(r.keys()))

def oneCSVRecord(r, fields):
     s = ','
     ensureFields(r, fields)
     return s.join([str(r[x]) for x in fields])

def lookup(dic, keys):
    if len(keys) > 1:
        return lookup(dic.get(keys[0], {}), keys[1:])
    return dic.get(keys[0])

def allCSVRecord(r, fields, nodes):
    s = ','
    return s.join([oneCSVRecord(lookup(r, node), fields) for node in nodes])

fields = ['count', 'minimumMicros', 'maximumMicros', 'meanMicros', 'populationStdDev']
nodes = [['docNoop', 'dnoop'], ['simpleNoop', 'snoop'], ['intNoop', 'inoop'], ['ping', 'ping']]

out = open("mwg.csv", "w")
for node in nodes:
    nodeprefix = node[1]
    s = ','
    out.write(s.join([nodeprefix + "-" + field for field in fields])+',')

out.write('\n')

for i in range(1000):
    name= 'results.json.' + str(i)
    r = json.load(open(name))
    out.write(allCSVRecord(r['main'], fields, nodes) + '\n')

out.close()
