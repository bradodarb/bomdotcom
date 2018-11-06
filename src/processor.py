from typing import Iterator, List

from src.line_handlers.line_handler import BomLineHandler
from src.logger import log
from src.util.errors import HandlerValidationException, HandlerNotFoundException
from src.util.parse_event import BomEvent


class BomProccessor:
    """
    Handles parsing a stream of textual BOM data into structured data
    """
    def __init__(self, records: Iterator[str], handlers: List[BomLineHandler], listeners:list=None):
        self._handlers = handlers
        self._current_handler = 0
        self._state = {
            'records': [],
            'failures': []
        }

        if listeners:
            self.bom_event = BomEvent()
            for listener in listeners:
                self.bom_event += listener

        self.process = self.process(records)

    @property
    def records(self):
        return self._state.get('records')

    @property
    def failures(self):
        return self._state.get('failures')

    @property
    def result(self):
        return self._state

    @property
    def handler(self) -> BomLineHandler:
        return self._handlers[self._current_handler]

    def _next_handler(self):
        """
        Simple round-robin handler selection
        Heuristics could be added to better select the handler most likely to be used next
        :return: None
        """
        self._current_handler += 1
        if self._current_handler > (len(self._handlers) - 1):
            self._current_handler = 0

    def process(self, records: Iterator[str]):
        """
        Iterates through records and builds a BOM (list of part data dicts)
        :param records: lines from a BOM file
        :return: None
        """
        for record in records:
            result = None
            attempts = len(self._handlers)
            while result is None:
                try:
                    if attempts < 0:
                        raise HandlerNotFoundException('No handler found')
                    result = self.handler.parse(self._state, record)
                    log.debug('Record Parse Attempted', f'{str(self.handler)} tried parsing {record}',
                              record=record, result=result)
                    if result:
                        self._state['records'].append(result)
                        self._notify(record, result)
                    else:
                        self._next_handler()
                except HandlerNotFoundException as nerr:
                    # log.exception(nerr, record=record)
                    self._state['failures'].append({
                        'line': record,
                        'handler': str(self._current_handler)
                    })
                    break
                except (HandlerValidationException, BaseException) as err:
                    self._next_handler()
                attempts -= 1

    def _notify(self, line: str, record: dict = None):
        """
        Notify concerned entities that a record has been parsed
        :param line: original str
        :param record: newly parsed record
        :return: None
        """
        try:
            if self.bom_event:
                self.bom_event(sender=self, line=line, record=record, state=self._state)
        except AttributeError as aerr:
            log.error('Invalid BOM Notification', str(aerr))
        except BaseException as err:
            log.exception(err)