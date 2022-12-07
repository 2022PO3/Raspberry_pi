import logging

from logging import Logger, RootLogger, WARNING, Manager

root = RootLogger(WARNING)
MSG_LENGTH = 55


class RPILoggerManager(Manager):
    def __init__(self, rootnode: RootLogger) -> None:
        super().__init__(rootnode)


class RPiLogger(Logger):
    manager = RPILoggerManager

    def __init__(self, *args) -> None:
        super().__init__(*args)

    def info(self, msg, *args, **kwargs) -> None:
        msg += " " * (MSG_LENGTH - len(msg))
        print("executing function")
        return super().info(msg, *args, **kwargs)


def getLogger(name=None) -> RPiLogger:
    """
    Return a logger with the specified name, creating it if necessary.

    If no name is specified, return the root logger.
    """
    if not name or isinstance(name, str) and name == root.name:
        return root
    return RPiLogger.manager.getLogger(name)


#################
# Logger config #
#################
def get_logger(name: str) -> logging.Logger:
    log_format = "%(asctime)s: %(message)s (%(name)8s)"
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        filename="rpi_garage.log",
        filemode="w",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    return getLogger(name)
