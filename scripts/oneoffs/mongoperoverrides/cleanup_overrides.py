import json
import os.path

def read_overrides_file(filename):
    with open(filename) as perf:
        overrides = json.load(perf)
    return overrides

def write_overrides_file(filename, overrides):
    with open(filename, 'w') as out:
        json.dump(
            overrides,
            out,
            indent=4,
            separators=[',', ':'],
            sort_keys=True)

def remove_ndays_baselines(filename):
    overrides = read_overrides_file(filename)
    for variant, var_over in overrides.iteritems():
        for task, task_over in var_over.iteritems():
            if 'ndays' in task_over:
                del task_over['ndays']
            if 'reference' in task_over:
                del task_over['reference']
    write_overrides_file(filename, overrides)

for branch in ['v4.0', 'v3.6', 'v3.4', 'v3.2', 'v3.0']:
    for file in ['system_perf_override.json', 'perf_override.json']:
        remove_ndays_baselines(os.path.join(branch, file))
