"""
BOM Base line parser

"""
import abc

MPN = 'MPN'
MANUFACTURER = 'Manufacturer'
REFERENCE_DESIGNATORS = 'ReferenceDesignators'
NUM_OCCURRENCES = 'NumOccurrences'


class BomLineHandler:
    """
    Represents a basic contract for converting lines of text into part models
    """
    @abc.abstractmethod
    def parse(self, state: dict, line: str):
        """
        Should try to parse and add the result to the appropriate section of the state dict
        :param state: Parsing result state
        :param line: single line of text to parse
        :return: result to indicate that parsing was successful
        """
        raise NotImplementedError


class ReportLimitHandler(BomLineHandler):
    """
    Handler that tries to parse a report limit parameter (simply an int in this test case)
    Simple example on how handlers can be implemented to modify state but aren't necessarily just for parsing part data
    """

    def parse(self, state: dict, line: str):
        """
        If the line can be entirely converted into an <int>, we will assume this should be setting the report_limit
        :param state: Parsing result state
        :param line: single line of text to parse
        :return: result to indicate that parsing was successful
        """
        try:
            result = int(line)
            state['report_limit'] = result
        except ValueError:
            pass
