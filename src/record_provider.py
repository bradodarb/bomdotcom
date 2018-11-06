import abc
import sys

from src.logger.slog import StructLog

logger = StructLog()


class RecordProvider:

    @abc.abstractmethod
    def records(self):
        raise NotImplementedError


class StdInRecordProvider(RecordProvider):

    def records(self):
        for line in sys.stdin:
            yield line


class FileRecordProvider(RecordProvider):

    def __init__(self, file_name: str):
        self._file_name = file_name

    def records(self):
        with open(self._file_name, 'r') as records:
            for record in records:
                yield record
