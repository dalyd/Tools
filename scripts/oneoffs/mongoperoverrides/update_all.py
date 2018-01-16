#!/bin/env python2.7
"""
This is a module.
"""

import datetime
import json
import os.path

import dateutil.parser
import pytz


def clean_ndays(overrides):
    """Delete all nday overrides that are no longer relevant.

    :param overrides: The overrides dictionary
    :returns: The updated overrides
    :rtype: dict

    """
    this_time = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
    for _build_variant, build_variant_overrides in overrides.iteritems():
        for _task, task_overrides in build_variant_overrides.iteritems():
            ndays = task_overrides['ndays']
            for test in ndays.keys():
                # Note: iterating over keys rather than iteritems so that we can delete the item.
                # You cannot do that while iterating over the items themselves.
                override = ndays[test]
                override_time = dateutil.parser.parse(override['create_time'])
                if (override_time + datetime.timedelta(days=7)) < this_time:
                    # Delete the nday override. It's out of date at this point.
                    print("Deleting ndays for variant={}, task={}, test={}".
                          format(_build_variant, _task, test))
                    del ndays[test]


# def traverse_overrides(overrides):
#     """ Traverse all the references overrides and update them

#     :param overrides: The overrides dictionary
#     :returns: The updated overrides
#     :rtype: dict

#     """

#     for build_variant, build_variant_overrides in overrides.iteritems():
#         for task, task_overrides in build_variant_overrides.iteritems():


def load_file(filename="master/system_perf_override.json"):
    """Load the file

    :param file:
    :returns: Overrides
    :rtype: dict

    """
    with open(filename) as filehandle:
        return json.load(filehandle)


def save_file(overrides, filename="master/system_perf_override.json"):
    """Load the file

    :param overrides:
    :param filename:
    :returns: Overrides
    :rtype: dict

    """
    with open(filename, 'w') as filehandle:
        json.dump(
            overrides,
            filehandle,
            indent=4,
            separators=[',', ':'],
            sort_keys=True)


def clean_all_ndays():
    """Iterate over all the override files and clean out old ndays
    :returns:
    :rtype:
    """
    branches = ['master', 'v3.6', 'v3.4', 'v3.2', 'v3.0']
    override_files = ['system_perf_override.json', 'perf_override.json']
    for branch in branches:
        for override_filename in override_files:
            # This assumes you are running in the analysis directory
            filename = os.path.join(branch, override_filename)
            if os.path.exists(filename):
                overrides = load_file(filename)
                clean_ndays(overrides)
                # Save the file back
                save_file(overrides, filename)
