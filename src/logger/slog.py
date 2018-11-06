"""
Wrapper and bootstrapper for structlog
"""
import logging

import structlog
from pythonjsonlogger import jsonlogger

MAX_LOG_OUTPUT = 20000
MAX_LOG_APPEND = ' ...'


class StructLog:
    """
    Reasonable settings for structured logger with a flent interface
    """

    def __init__(self, logger_key: str='Application'):
        structlog.configure(
            processors=[
                structlog.stdlib.filter_by_level,
                structlog.stdlib.add_logger_name,
                structlog.stdlib.add_log_level,
                structlog.stdlib.PositionalArgumentsFormatter(),
                structlog.processors.StackInfoRenderer(),
                structlog.processors.format_exc_info,
                structlog.processors.UnicodeDecoder(),
                structlog.stdlib.render_to_log_kwargs,
            ],
            context_class=dict,
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.stdlib.BoundLogger,
            cache_logger_on_first_use=True,
        )

        handler = logging.StreamHandler()
        handler.setFormatter(jsonlogger.JsonFormatter())

        logger = logging.getLogger()
        logger.addHandler(handler)

        self.log = structlog.get_logger(logger_key)

    def _fit_log_msg(self, msg, limit_output):
        """
        Trims the log based on maximum length declared for messages
        """
        if not limit_output:
            return msg
        msg_str = str(msg)
        return (msg_str[:MAX_LOG_OUTPUT] +
                MAX_LOG_APPEND) if len(msg_str) > MAX_LOG_OUTPUT else msg

    def bind(self, **value):
        """
        add binding arguments to structured logger
        """
        self.log.bind(**value)

    def exception(self, error, **kwargs):
        """
        log exception to structure logger
        """
        self.log.error('EXCEPTION',
                       error_type=type(error).__name__,
                       verbose_msg=str(error),
                       exc_info=True,
                       **kwargs)

        return self

    def critical(self, event, msg, limit_output=True, **kwargs):
        """
        log critical to structure logger
        """
        self.log.critical(self._fit_log_msg(event,
                                            limit_output),
                          interim_desc=self._fit_log_msg(msg,
                                                         limit_output),
                          **kwargs)

        return self

    def error(self, event, msg, limit_output=True, **kwargs):
        """
        log error to structure logger
        """
        self.log.error(self._fit_log_msg(event,
                                         limit_output),
                       interim_desc=self._fit_log_msg(msg,
                                                      limit_output),
                       **kwargs)

        return self

    def warn(self, event, msg, limit_output=True, **kwargs):
        """
        log warn to structure logger
        """
        self.log.warning(self._fit_log_msg(event,
                                           limit_output),
                         interim_desc=self._fit_log_msg(msg,
                                                        limit_output),
                         **kwargs)

        return self

    def info(self, event, msg, limit_output=True, **kwargs):
        """
        log info to structure logger
        """
        self.log.info(self._fit_log_msg(event,
                                        limit_output),
                      interim_desc=self._fit_log_msg(msg,
                                                     limit_output),
                      **kwargs)

        return self

    def debug(self, event, msg, limit_output=True, **kwargs):
        """
        log debug to structure logger
        """
        self.log.debug(self._fit_log_msg(event,
                                         limit_output),
                       interim_desc=self._fit_log_msg(msg,
                                                      limit_output),
                       **kwargs)

        return self
