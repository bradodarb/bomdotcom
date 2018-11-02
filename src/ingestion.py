import abc


class BomLineHandler:
    def __init__(self, next=None):
        self._next = next

    def handle_line(self, state: dict, line: str):
        result = self._handle_line(state, line)
        if result:
            return result
        else:
            return self.handle_line()

    @abc.abstractmethod
    def _handle_line(self, state: dict, line: str):
        raise NotImplementedError


class ReportLimitCommandHandler(BomLineHandler):
    """
    Handler that tries to parse a report limit parameter (simply int in this case)
    """
    def _handle_line(self, state: dict, line: str):
        try:
            result = int(line)
            state['report_limit'] = result
            return result
        except ValueError:
            return False