"""
Module to facilitate subscribing to BOM events
"""


class BomEvent:
    """
    Allows multiple notifiers to subscribe to an event of interest
    """

    def __init__(self):
        self.handlers = []

    def add(self, handler):
        """
        Adds an event to the list of subscribers
        :param handler:
        :return: self
        """
        self.handlers.append(handler)
        return self

    def remove(self, handler):
        """
        Removes an event to the list of subscribers
        :param handler:
        :return: self
        """
        self.handlers.remove(handler)
        return self

    def notify(self, sender, line: str, record: dict, state: dict):
        """
        Notify subscribers of a change
        :param sender: caller
        :param line: str
        :param record: dict
        :param state: dict
        :return: None
        """
        for handler in self.handlers:
            handler(sender=sender, line=line, record=record, state=state)

    __iadd__ = add
    __isub__ = remove
    __call__ = notify
