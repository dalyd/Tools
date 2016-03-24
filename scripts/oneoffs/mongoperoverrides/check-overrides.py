#!/bin/python

import itertools
import json
from evergreen import override

#assumes in DSI/analysis
overrides = json.load(open("master/perf_override.json"))

st_ref = overrides['linux-wt-standalone']['reference']

# This gives a list of tickets total. 
[test['ticket'] for (name, test) in st_ref.items() if 'ticket' in test.keys()]

list(itertools.chain([test['ticket'] for (name, test) in st_ref.items() if 'ticket' in test.keys()]))
[ticket for ticket in test['ticket'] for (name, test) in st_ref.items() if 'ticket' in test.keys()]

# This gets the name of all the things that aren't in a list. 
[name for (name, test) in st_ref.items() if 'ticket' in test.keys() and not isinstance(test['ticket'], list)]

[test['ticket'] for (name, test) in st_ref.items() if 'ticket' in test.keys() and not isinstance(test['ticket'], list)]
# Need to flatten this one
[test['ticket'] for (name, test) in st_ref.items() if 'ticket' in test.keys() and isinstance(test['ticket'], list)]
list(itertools.chain(*[test['ticket'] for (name, test) in st_ref.items() if 'ticket' in test.keys() and isinstance(test['ticket'], list)]))

# Here we go. 
set(itertools.chain(*[test['ticket'] for (name, test) in st_ref.items() if 'ticket' in test.keys() and isinstance(test['ticket'], list)]))

#This cleans things up. Need to scale it for the whole file. 
for (name, test) in st_ref.items():
    if 'ticket' in test.keys() and not isinstance(test['ticket'], list):
        st_ref[name]['ticket'] = list(test['ticket'])
        

# Reset all ndays
for (variant_key, variant_value) in overrides.items():
    variant_value['ndays'] = {}

#Clean up all overrides tickets. 
for (variant_key, variant_value) in overrides.items():
    ref = variant_value['reference']
    for (name, test) in ref.items():
        if 'ticket' in test.keys() and not isinstance(test['ticket'], list):
            test['ticket'] = [test['ticket']]


tickets = set()
for (variant_key, variant_value) in overrides.items():
    ref = variant_value['reference']
    tickets = tickets.union(set(itertools.chain(*[test['ticket'] for (name, test) in ref.items() if
                                                  'ticket' in test.keys() and 
                                                  isinstance(test['ticket'], list)])))

o = override.Override(overrides)
o.save_to_file("master/perf_override.json")
