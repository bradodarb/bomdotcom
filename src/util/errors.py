class HandlerNotFoundException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)


class HandlerValidationException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
