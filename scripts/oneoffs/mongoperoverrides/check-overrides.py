#!/bin/python

import itertools
import json
from evergreen import override

#assumes in DSI/analysis
overrides = json.load(open("master/perf_override.json"))

st_ref = overrides['linux-wt-standalone']['reference']

# This gives a list of tickets total.
# [test['ticket'] for (name, test) in st_ref.items() if 'ticket' in test.keys()]

# list(itertools.chain([test['ticket'] for (name, test) in st_ref.items() if 'ticket' in test.keys()]))
# [ticket for ticket in test['ticket'] for (name, test) in st_ref.items() if 'ticket' in test.keys()]

# # This gets the name of all the things that aren't in a list.
# [name for (name, test) in st_ref.items() if 'ticket' in test.keys() and not isinstance(test['ticket'], list)]

# [test['ticket'] for (name, test) in st_ref.items() if 'ticket' in test.keys() and not isinstance(test['ticket'], list)]
# # Need to flatten this one
# [test['ticket'] for (name, test) in st_ref.items() if 'ticket' in test.keys() and isinstance(test['ticket'], list)]
# list(itertools.chain(*[test['ticket'] for (name, test) in st_ref.items() if 'ticket' in test.keys() and isinstance(test['ticket'], list)]))

# # Here we go.
# set(itertools.chain(*[test['ticket'] for (name, test) in st_ref.items() if 'ticket' in test.keys() and isinstance(test['ticket'], list)]))

# #This cleans things up. Need to scale it for the whole file.
# for (name, test) in st_ref.items():
#     if 'ticket' in test.keys() and not isinstance(test['ticket'], list):
#         st_ref[name]['ticket'] = list(test['ticket'])

# Clean up reference overrides that aren't dictionaries. 
def clean_bad_entries(overrides):
    ''' Remove entries that aren't a dictionary'''
    for variant_value in overrides.values():
        ref = variant_value['reference']
        variant_value['reference'] = {name: test for (name, test) in ref.items() if
                                      isinstance(ref[name], dict)}
def find_non_ticketed(overrides):
    ''' print out all entries without a ticket field'''
    for build_variant in overrides:
        for rule in overrides[build_variant]:
            print "{} {}".format(build_variant, rule)
            print ([name for name in overrides[build_variant][rule] if 'ticket' not in
                    overrides[build_variant][rule][name]])


def reset_ndays(overrides):
    """ Remove all ndays overrides
    Should be extended to remove all non-expired nday overrides, rather than all
    """
    for (variant_key, variant_value) in overrides.items():
        variant_value['ndays'] = {}
    return overrides

def remove_non_ticketed(overrides):
    ''' Delete overrides that don't have a ticket entry'''
    for build_variant in overrides:
        for rule in overrides[build_variant]:
            overrides[build_variant][rule] = {name: test for (name, test) in
                                              overrides[build_variant][rule].items() if 'ticket'
                                              in test}

def fix_non_list_tickets(overrides):
    """ Fix and occurrences with tickets as a string rather than a list
    """
    #Clean up all overrides tickets.
    for (variant_key, variant_value) in overrides.items():
        ref = variant_value['reference']
        for (name, test) in ref.items():
            if 'ticket' in test.keys() and not isinstance(test['ticket'], list):
                test['ticket'] = [test['ticket']]
    return (overrides)

def get_tickets(overrides, rule='reference'):
    """ Return a list of all tickets mentioned in overrides """
    tickets = set()
    for (variant_key, variant_value) in overrides.items():
        print variant_key
        ref = variant_value[rule]
        tickets = tickets.union(set(itertools.chain(*[test['ticket'] for (name, test) in ref.items() if
                                                      'ticket' in test.keys() and
                                                      isinstance(test['ticket'], list)])))
    return (tickets)

def get_tests_by_ticket(overrides, ticket):
    '''
    Get list of tests with the given ticket
    '''
    
    tests = {}
    for build_variant in overrides:
        tests[build_variant] = {}
        for rule in overrides[build_variant]:
            rule_tests = set()
            # Remove anything that can be blanket removed. Can't otherwise remove from something we're iterating over
            overrides[build_variant][rule] = {name: test for (name, test) in overrides[build_variant][rule].items()
                                              if 'ticket' in test and
                                              test['ticket'].count(ticket) != len(test['ticket'])}
            for test in overrides[build_variant][rule]:
                #Look to see if it should be pulled from the ticket list
                if 'ticket' in overrides[build_variant][rule][test]:
                    print test
                    rule_tests.add(test)
            if len(rule_tests) > 0:
                tests[build_variant][rule] = rule_tests
    return tests

def delete_overrides_by_ticket(overrides, ticket):
        """Remove the overrides created by a given ticket.

        :param str ticket: The ID of a JIRA ticket (e.g. SERVER-20123)
        """
        for build_variant in overrides:
            for rule in overrides[build_variant]:
                # Remove anything that can be blanket removed. Can't otherwise remove from something we're iterating over
                overrides[build_variant][rule] = {name: test for (name, test) in overrides[build_variant][rule].items()
                                                  if 'ticket' in test and
                                                  test['ticket'].count(ticket) != len(test['ticket'])}
                for test in overrides[build_variant][rule]:
                    #Look to see if it should be pulled from the ticket list
                    if 'ticket' in overrides[build_variant][rule][test]:
                        if ticket in overrides[build_variant][rule][test]['ticket']:
                            overrides[build_variant][rule][test]['ticket'].remove(ticket)
                    
o = override.Override(overrides)
o.save_to_file("master/perf_override.json")

