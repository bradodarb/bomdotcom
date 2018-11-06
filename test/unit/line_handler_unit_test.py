import asyncio
import os
import unittest

from src.line_handlers.line_handler import ReportLimitHandler, BomLineHandler
from src.logger import log


class TestLineHandlers(unittest.TestCase):

    def setUp(self):
        os.environ['LOG_LEVEL'] = 'DEBUG'
        self.loop = asyncio.get_event_loop()
        log.info("======   Test: %s, SetUp", self.id())

    def tearDown(self):
        log.info("------   Test: %s, TearDown", self.id())

    def test_BomLineHandler_throws_not_implemented(self):
        state = {}
        handler = BomLineHandler()

        with self.assertRaises(NotImplementedError):
            handler.parse(state, '1234')

    def test_ReportLimitCommandHandler(self):
        state = {}

        handler = ReportLimitHandler()

        handler.parse(state, '123')

        self.assertEqual(state['report_limit'], 123)

    def test_ReportLimitCommandHandler_fails(self):
        state = {}

        handler = ReportLimitHandler()

        handler.parse(state, '123 records')
        with self.assertRaises(KeyError):
            self.assertEqual(state['report_limit'], 123)


if __name__ == '__main__':
    unittest.main()
