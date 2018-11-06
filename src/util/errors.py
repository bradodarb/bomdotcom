"""
Line processing errors
"""
class HandlerNotFoundException(Exception):
    """
    This should be called if a line cannot be parsed by a processor
    """
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)


class HandlerValidationException(Exception):
    """
    This should be called if a line cannot be parsed by a given handler
    """
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
