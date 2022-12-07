import logging


#################
# Logger config #
#################
def get_logger(name: str) -> logging.Logger:
    log_format = "%(asctime)s: %(message)s (%(name)8s)"
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        filename="rpi_garage.log",
        filemode="a",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    return logging.getLogger(name)


def justify_logs(msg: str, length: int = 55) -> str:
    return msg + " " * (length - len(msg))
