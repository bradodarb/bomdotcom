"""
Example report for part data analytics
This is not optimal as it adds another cycle through the already processed records
Report layer should be implemented via events when possible
"""

from src.line_handlers.line_handler import (MPN, MANUFACTUREER, REFERENCE_DESIGNATORS, NUM_OCCURRENCES)
from src.logger import LOG


def format_key(record: dict):
    """
    Builds key hash for part
    :param record: dict
    :return: str
    """
    return f'{record[MPN]}::{record[MANUFACTUREER]}'


def rank_report(source: dict):
    """
    Compiles, sorts and ouputs the report results
    :param source: dict
    :return:
    """
    try:
        results = {}
        for record in source['records']:
            key = format_key(record)
            if key in results:
                results[key]['part'][NUM_OCCURRENCES] += 1

                results[key]['part'][REFERENCE_DESIGNATORS] = list(set(
                    results[key]['part'][REFERENCE_DESIGNATORS] + record[REFERENCE_DESIGNATORS]))

                results[key]['rank'] = results[key]['part'][NUM_OCCURRENCES] + len(
                    results[key]['part'][REFERENCE_DESIGNATORS])

            else:
                results[key] = {
                    'part': record,
                    'rank': record[NUM_OCCURRENCES] + len(record[REFERENCE_DESIGNATORS])
                }

        output = list(sorted(results, key=lambda x: results[x]['rank'], reverse=True))

        cursor = 0

        while cursor < source['report_limit']:
            yield results[output[cursor]]['part']
            cursor += 1
    except (KeyError, BaseException) as err:
        LOG.exception(err)
