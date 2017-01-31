#!/usr/bin/env python

'''Take agg_results.json and flatten it into an array of documents
suitable for import into mongo

'''
import copy
import json

def load_data(filename='agg_results.json'):
    ''' Loads in result data'''
    with open(filename) as input_file:
        results = json.load(input_file)
    return results

def flatten(results, labels={}):
    '''Flatten the results into a list of documents. Assumes the results
    have keys going variant, task, test, thread level.

    :param: dict result: The results file to flatten.
    :param: dict labels: Extra entries to include in each document

    '''
    flat_results = []
    for variant_name, variant in results.iteritems():
        for task_name, task in variant.iteritems():
            for test_name, test in task.iteritems():
                for thread_level, thread_results in test.iteritems():
                    new_doc = copy.deepcopy(thread_results)
                    new_doc['thread_level'] = thread_level
                    new_doc['test_name'] = test_name
                    new_doc['task_name'] = task_name
                    new_doc['variant_name'] = variant_name
                    new_doc.update(labels)
                    flat_results.append(new_doc)
    return flat_results

def main():
    '''
    main
    '''
    results = load_data()
    with open('flat.json', 'w') as output:
        json.dump(flatten(results), output, indent=4, sort_keys=True)

if __name__ == '__main__':
    main()
