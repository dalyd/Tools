import json
r = json.load(open("results.json"))


def printCSVRecord(r, fields, out): 
    ''' Print out one result record in CSV delimited form. Just the one entry'''
    s = ','
    out.write(s.join([str(r[x]) for x in fields])+'\n')

def ensureFields(r, fields): 
    ''' Make sure all the fields exist in M. Insert 0 if not '''
    r.update((missing, 0) for missing in set(fields).difference(r.keys()))


fields = ['count', 'min', 'max', 'mean', 'popStdDev']
out = open("test.out", "w")
s=','
out.write(s.join(fields)+ '\n')
for rec in r : 
    ensureFields(rec['main']['insert2'],  fields)
    printCSVRecord(rec['main']['insert2'], fields, out)

out.close()
