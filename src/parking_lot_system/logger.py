import logging

from logging import Logger, RootLogger, WARNING

root = RootLogger(WARNING)
MSG_LENGTH = 55


class RPiLogger(Logger):
    def __init__(self, *args) -> None:
        super().__init__(*args)

    def info(self, msg: object, *args, **kwargs) -> None:
        msg += " " * (MSG_LENGTH - len(msg))
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
