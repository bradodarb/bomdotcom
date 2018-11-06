"""
Example report for part data analytics implemeneted as
"""

from src.line_handlers.line_handler import (MPN, Manufacturer, ReferenceDesignators, NumOccurrences)
from src.logger import log


class RunningRankingReport:
    """
    Subscribes to a BOM parsing processor and incrementally builds a report
    """
    def __init__(self):
        self.results = {}
        self.report_limit = 1

    def on_bom_record(self, sender, line: str, record: dict, state: dict):
        """
        Fires each time a record is successfully parsed
        :param sender: event emitter
        :param line: str
        :param record: dict
        :param state: dict
        :return:
        """
        if state:
            self.report_limit = state.get('report_limit', self.report_limit)
        if record:
            key = RunningRankingReport.format_key(record)
            if key in self.results:
                self.results[key]['part'][NumOccurrences] += 1

                self.results[key]['part'][ReferenceDesignators] = list(set(
                    self.results[key]['part'][ReferenceDesignators] + record[ReferenceDesignators]))

                self.results[key]['rank'] = self.results[key]['part'][NumOccurrences] + len(
                    self.results[key]['part'][ReferenceDesignators])

            else:
                self.results[key] = {
                    'part': record,
                    'rank': record[NumOccurrences] + len(record[ReferenceDesignators])
                }

    def run(self):
        """
        Sorts and ouputs the report results
        :return:
        """
        output = list(sorted(self.results, key=lambda x: self.results[x]['rank'], reverse=True))

        cursor = 0

        while cursor < self.report_limit:
            yield self.results[output[cursor]]['part']
            cursor += 1

    @staticmethod
    def format_key(record: dict):
        """
        Builds key hash for part
        :param record: dict
        :return: str
        """
        return f'{record[MPN]}::{record[Manufacturer]}'

    __call__ = on_bom_record
