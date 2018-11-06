""""
Module for ingesting BOM data
"""
import abc
import sys


class RecordProvider:
    """
    Interface for ingesting BOM data
    """

    @abc.abstractmethod
    def records(self):
        """
        Access point for obtaining records from a given source
        :return: [str]
        """
        raise NotImplementedError


class StdInRecordProvider(RecordProvider):
    """
    Ingesting BOM data from STDin
    """

    def records(self):
        """
        Access point for obtaining records from a stdin
        :return: [str]
        """
        for line in sys.stdin:
            yield line


class FileRecordProvider(RecordProvider):
    """
    Ingesting BOM data from file
    """

    def __init__(self, file_name: str):
        self._file_name = file_name

    def records(self):
        """
        Access point for obtaining records from file
        :return: [str]
        """
        with open(self._file_name, 'r') as records:
            for record in records:
                yield record
