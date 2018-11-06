"""
BOM Regex line parser and utils
"""
import re
from collections import OrderedDict
from typing import Callable

from src.line_handlers.line_handler import (MPN, MANUFACTUREER, REFERENCE_DESIGNATORS, NUM_OCCURRENCES, BomLineHandler)
from src.util.errors import HandlerValidationException


class RegExBomLineHandler(BomLineHandler):
    """
    Flexible line parser strategy that uses regex and an index map to parse text into part models
    """
    _split_pattern = re.compile('[,;:]| -- ')

    def __init__(self, part_map: dict, validator: Callable = None):
        """
        Set the index map and the validation function
        :param part_map: dict for matching keys to array indices
        :param validator: validation check to see if this handler is suitable
        """
        self.part_map = part_map
        self.validator = validator

    def parse(self, state: dict, line: str):
        self._validate(line)

        parts = re.split(RegExBomLineHandler._split_pattern, line)

        result = OrderedDict()

        result[MPN] = parts[self.part_map[MPN]].strip()
        result[MANUFACTUREER] = parts[self.part_map[MANUFACTUREER]].strip()
        result[REFERENCE_DESIGNATORS] = []
        result[NUM_OCCURRENCES] = 1

        exclusions = [result[MANUFACTUREER], result[MPN]]

        for part in parts:
            part = part.strip()
            if part not in exclusions:
                result[REFERENCE_DESIGNATORS].append(part)

        result[REFERENCE_DESIGNATORS].sort()
        return result

    def _validate(self, line: str):
        """
        Validate line input
        :param line: str-> raw input line from BOPM
        :return: raise if this handler is unsuitable for parsing record
        """
        if self.validator:
            if not self.validator(line):
                raise HandlerValidationException('Parsing constraints not satisfied for this handler')
