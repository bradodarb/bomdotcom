import os
import unittest

from src.line_handlers.line_handler import ReportLimitHandler
from src.line_handlers.re_line_handler import RegExBomLineHandler
from src.logger import LOG
from src.processor import BomProccessor
from src.record_provider import FileRecordProvider
from src.line_handlers.line_handler import (MPN, MANUFACTURER, REFERENCE_DESIGNATORS)
from src.reports.rank_report import rank_report
from src.reports.running_rank_report import RunningRankingReport


class TestProcessor(unittest.TestCase):

    def setUp(self):
        os.environ['LOG_LEVEL'] = 'DEBUG'
        LOG.info("======   Test: %s, SetUp", self.id())

    def tearDown(self):
        LOG.info("------   Test: %s, TearDown", self.id())

    def test_BomProccessor_with_report_handler(self):
        handler = BomProccessor(FileRecordProvider('./test/test_data/bom.com').records(), [ReportLimitHandler()])

        self.assertTrue(len(handler.records) == 0)

        self.assertEqual(handler.result['report_limit'], 2)

    def test_BomProccessor_with_regex_handler_and_rank_report(self):
        handler = BomProccessor(FileRecordProvider('./test/test_data/bom.com').records(),
                                [
                                    ReportLimitHandler(),
                                    RegExBomLineHandler({
                                        MPN: 0,
                                        MANUFACTURER: 1
                                    }, lambda line: line.count(':') == 2),
                                    RegExBomLineHandler({
                                        MPN: -2,
                                        MANUFACTURER: -1
                                    }, lambda line: line.count(';') == 2),
                                    RegExBomLineHandler({
                                        MPN: 1,
                                        MANUFACTURER: 0
                                    }, lambda line: line.count(' -- ') == 1 and line.count(':') >= 1)
                                ])
        self.assertTrue(len(handler.records) == 4)

        report = rank_report(handler.result)

        results = list(report)
        self.assertIsNotNone(results)
        self.assertEqual(len(results), 2)

    def test_BomProccessor_with_regex_handler_and_running_rank_report(self):
        report = RunningRankingReport()
        handler = BomProccessor(FileRecordProvider('./test/test_data/bom.com').records(),
                                [
                                    ReportLimitHandler(),
                                    RegExBomLineHandler({
                                        MPN: 0,
                                        MANUFACTURER: 1
                                    }, lambda line: line.count(':') == 2),
                                    RegExBomLineHandler({
                                        MPN: -2,
                                        MANUFACTURER: -1
                                    }, lambda line: line.count(';') == 2),
                                    RegExBomLineHandler({
                                        MPN: 1,
                                        MANUFACTURER: 0
                                    }, lambda line: line.count(' -- ') == 1 and line.count(':') >= 1)
                                ], listeners=[report])

        self.assertTrue(len(handler.records) == 4)
        results = list(report.run())

        self.assertIsNotNone(list(results))
        self.assertEqual(len(list(results)), 2)


if __name__ == '__main__':
    unittest.main()
