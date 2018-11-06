import asyncio
import sys
import os
import unittest

from src.logger import log
from src.record_provider import FileRecordProvider, StdInRecordProvider, RecordProvider


class TestRecordProviders(unittest.TestCase):

    def setUp(self):
        os.environ['LOG_LEVEL'] = 'DEBUG'
        self.loop = asyncio.get_event_loop()
        log.info("======   Test: %s, SetUp", self.id())

    def tearDown(self):
        log.info("------   Test: %s, TearDown", self.id())

    def test_RecordProvider_throws_not_implemented(self):
        provider = RecordProvider()

        with self.assertRaises(NotImplementedError):
            for record in provider.records():
                self.assertIsNotNone(record)

    def test_FileRecordProvider(self):
        provider = FileRecordProvider('./test/test_data/bom.com')

        result = []

        for record in provider.records():
            result.append(record)

        self.assertEqual(len(result), 5)

    def test_StdInRecordProvider(self):
        sys.stdin = open('./test/test_data/bom.com')
        provider = StdInRecordProvider()

        result = []

        for record in provider.records():
            result.append(record)

        self.assertEqual(len(result), 5)

        sys.stdin.close()


if __name__ == '__main__':
    unittest.main()
