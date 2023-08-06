import logging


def getHandlerConfig(className: str, level: str = None, formatter: str = None,
            filters: list = None, **kwargs) -> dict:
    """Create and return a handler config.

    Parameters
    ----------
    className : str
        This is the fully qualified name of the handler class.
    level : str, optional
        The level of the handler, by default None
    formatter : str, optional
        The id of the formatter for this handler, by default None
    filters : list, optional
        A list of ids of the filters for this handler, by default None

    Returns
    -------
    dict
        handler config.
    """
    config = { "class": className }
    if level is not None:
        config["level"] = level
    if formatter is not None:
        config["formatter"] = formatter
    if filters is not None:
        config["filters"] = filters
    config.update(kwargs)
    return config


def getConsleHandlerConfig(level: str = None, formatter: str = None,
            stream: str = "ext://sys.stderr") -> dict:
    """Create and return a consle handler config.

    Parameters
    ----------
    level : str, optional
        The level of the handler, by default None
    formatter : str, optional
        The id of the formatter for this handler, by default None
    stream : str, optional
        The stream that the handler should use, by default "ext://sys.stderr"

    Returns
    -------
    dict
        consle handler config.
    """
    return getHandlerConfig(
        f"{ConsoleHandler.__module__}.{ConsoleHandler.__name__}",
        level,
        formatter,
        stream = stream
    )


def getFileHandlerConfig(filename: str, mode: str = "a", encoding: str = None,
            level: str = None, formatter: str = None, **kwargs) -> dict:
    """Create and return a file handler config.

    Parameters
    ----------
    filename : str
        log file name
    mode : str, optional
        log file open mode, by default "a"
    encoding : str, optional
        log file encoding, by default None
    level : str, optional
        The level of the handler, by default None
    formatter : str, optional
        The id of the formatter for this handler, by default None

    Returns
    -------
    dict
        file handler config.
    """
    config = {
        "filename": filename,
        "mode" : mode,
    }
    if encoding is not None:
        config["encoding"] = encoding
    return getHandlerConfig(
        f"{FileHandler.__module__}.{FileHandler.__name__}",
        level,
        formatter,
        filters=None,
        **config
    )


class ConsoleHandler(logging.StreamHandler):
    def __init__(self, stream=None):
        """
        A handler class which writes logging records, appropriately formatted,
        to a stream. Note that this class does not close the stream, as
        sys.stdout or sys.stderr may be used.

        Parameters
        ----------
        stream : _type_, optional
            output stream, by default None
        """
        super().__init__(stream=stream)


class FileHandler(logging.FileHandler):
    def __init__(self, filename: str, mode: str = "a", encoding: str = None,
                    delay: bool = False):
        """Create a file handler.

        Parameters
        ----------
        filename : str
            log file name
        mode : str, optional
            log file open mode, by default "a"
        encoding : str, optional
            log file encoding, by default None
        delay : bool, optional
            log file open delay, by default False
        """
        super().__init__(filename, mode=mode, encoding=encoding, delay=delay)
