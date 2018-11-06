"""
Example report for part data analytics implemeneted as
"""

from src.line_handlers.line_handler import (MPN, MANUFACTURER, REFERENCE_DESIGNATORS, NUM_OCCURRENCES)

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
                self.results[key]['part'][NUM_OCCURRENCES] += 1

                self.results[key]['part'][REFERENCE_DESIGNATORS] = list(set(
                    self.results[key]['part'][REFERENCE_DESIGNATORS] + record[REFERENCE_DESIGNATORS]))

                self.results[key]['rank'] = self.results[key]['part'][NUM_OCCURRENCES] + len(
                    self.results[key]['part'][REFERENCE_DESIGNATORS])

            else:
                self.results[key] = {
                    'part': record,
                    'rank': record[NUM_OCCURRENCES] + len(record[REFERENCE_DESIGNATORS])
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
        return f'{record[MPN]}::{record[MANUFACTURER]}'

    __call__ = on_bom_record
