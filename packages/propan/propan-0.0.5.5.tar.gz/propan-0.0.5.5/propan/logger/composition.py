from functools import wraps
from typing import Tuple
from inspect import iscoroutinefunction

from .model.usecase import LoggerUsecase


class LoggerSimpleComposition(LoggerUsecase):
    loggers: Tuple[LoggerUsecase]
    not_catch: Tuple[Exception]

    def __init__(
        self,
        *loggers: Tuple[LoggerUsecase, int],
        not_catch: Tuple[Exception] = tuple()
    ):
        self.loggers = loggers
        self.not_catch = not_catch
        for logger in self.loggers:
            logger.not_catch = not_catch

    def info(self, message: str):
        for logger in self.loggers:
            logger.info(message)

    def debug(self, message: str):
        for logger in self.loggers:
            logger.debug(message)

    def error(self, message: str):
        for logger in self.loggers:
            logger.error(message)

    def warning(self, message: str):
        for logger in self.loggers:
            logger.warning(message)

    def success(self, message: str):
        for logger in self.loggers:
            logger.success(message)

    def log(self, *args, **kwargs):
        for logger in self.loggers:
            logger.log(*args, **kwargs)

    def catch(self, func):
        new_func = func
        for logger in self.loggers[:-1]:
            new_func = wraps(func)(logger.catch)(new_func, reraise=True)
        new_func = wraps(self.loggers[-1].catch)(new_func)

        if iscoroutinefunction(func):
            @wraps(func)
            async def wrapped(*args, **kwargs):
                return await new_func(*args, **kwargs)
        else:
            @wraps(func)
            def wrapped(*args, **kwargs):
                return new_func(*args, **kwargs)

        return wrapped
