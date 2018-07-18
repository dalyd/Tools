'''
Scripts for accessing JIRA

Sample code:
from mjira import *
jira = login('david.daly', 'PASSWORD')
issues = team_issues(jira, expand='changelog')
[(issue.key, active_time(issue)) for issue in issues]

#Active time versus story points:
[(issue.key, issue.fields.customfield_10555, active_time(issue)) for issue in issues if hasattr(issue.fields, 'customfield_10555')]
#Active time for tickets without story points
[(issue.key, active_time(issue)) for issue in issues if not hasattr(issue.fields, 'customfield_10555')]

# Print time in hours.
>>> for item in [(issue.key, issue.fields.customfield_10555, active_time(issue).total_seconds()/3600) for issue in issues if hasattr(issue.fields, 'customfield_10555') and issue.fields.customfield_10555 is not None]:
...     print(item)


'''

import datetime
import dateutil.parser
from jira import JIRA

ACTIVE_STATUSES = [u'In Progress', u'In Code Review']


def login(username, password):
    ''' Login to JIRA '''
    return JIRA('https://jira.mongodb.org/', auth=(username, password))


def team_issues(jira, timeframe=None, expand=None):
    '''
    Get issues for the team.
    '''
    if timeframe is None:
        timeframe = '-30d'
    query = 'assignee in (membersOf(serverteam-perf)) and resolution is not Empty'
    query += ' and resolution was Empty after {}'.format(timeframe)
    return jira.search_issues(query, expand=expand)


def is_stop(history):
    '''
    Is this changelog history represent stopped progress. Going from In Progress or On Code Review
    out.

    '''
    for item in history.items:
        if (item.field == u'status' and item.fromString in ACTIVE_STATUSES
                and item.toString not in ACTIVE_STATUSES):
            return True
    return False


def is_start(history):
    '''
    Is this changelog history represent stopped progress. Going from In Progress or On Code Review
    out.

    '''
    for item in history.items:
        if (item.field == u'status' and item.fromString not in ACTIVE_STATUSES
                and item.toString in ACTIVE_STATUSES):
            return True
    return False


def start_times(issue):
    ''' Returns a list of times when progress started on this ticket.
    '''
    return [
        history.created for history in issue.changelog.histories
        if is_start(history)
    ]


def end_times(issue):
    ''' Returns a list of times when progress started on this ticket.
    '''
    return [
        history.created for history in issue.changelog.histories
        if is_stop(history)
    ]


def active_time(issue):
    '''
    Calculate how long an issue was active. Returns a timedelta.
    '''
    return sum((dateutil.parser.parse(end) - dateutil.parser.parse(start)
                for start, end in zip(start_times(issue), end_times(issue))),
               datetime.timedelta())
