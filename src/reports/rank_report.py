"""
Example report for part data analytics
This is not optimal as it adds another cycle through the already processed records
Report layer should be implemented via events when possible
"""

from src.line_handlers.line_handler import (MPN, Manufacturer, ReferenceDesignators, NumOccurrences)
from src.logger import log


def format_key(record: dict):
    """
    Builds key hash for part
    :param record: dict
    :return: str
    """
    return f'{record[MPN]}::{record[Manufacturer]}'


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
                results[key]['part'][NumOccurrences] += 1

                results[key]['part'][ReferenceDesignators] = list(set(
                    results[key]['part'][ReferenceDesignators] + record[ReferenceDesignators]))

                results[key]['rank'] = results[key]['part'][NumOccurrences] + len(
                    results[key]['part'][ReferenceDesignators])

            else:
                results[key] = {
                    'part': record,
                    'rank': record[NumOccurrences] + len(record[ReferenceDesignators])
                }

        output = list(sorted(results, key=lambda x: results[x]['rank'], reverse=True))

        cursor = 0

        while cursor < source['report_limit']:
            yield results[output[cursor]]['part']
            cursor += 1
    except (BaseException, Exception) as err:
        log.exception(err)
