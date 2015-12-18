import json
r = json.load(open("results.json"))


def printCSVRecord(r, fields, out): 
    ''' Print out one result record in CSV delimited form. Just the one entry'''
    s = ','
    out.write(s.join([str(r[x]) for x in fields])+'\n')

def ensureFields(r, fields): 
    ''' Make sure all the fields exist in M. Insert 0 if not '''
    r.update((missing, 0) for missing in set(fields).difference(r.keys()))

def lookup(dic, keys):
    if len(keys) > 1:
        return lookup(dic.get(keys[0], {}), keys[1:])
    return dic.get(keys[0])

def CSVForField(r, key, fields, out) : 
    ''' Create CSV File for the given key. Key is the list of keys to get to the right place '''
    s=','
    out.write(s.join(fields)+ '\n')
    for rec in r: 
        cur = lookup(rec, key)
        ensureFields(cur, fields)
        printCSVRecord(cur, fields, out)


fields = ['count', 'min', 'max', 'mean', 'popStdDev']

out = open("test.out", "w")
CSVForField(r, ["main", "insert2"], fields, out)

out.close()
