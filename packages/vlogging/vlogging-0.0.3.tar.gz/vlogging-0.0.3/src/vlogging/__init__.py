import logging
import logging.config
from typing import Any

from vlogging import (
    formatters,
    handlers,
    loggers,
)
from vlogging.loggers import Logger

from logging import (
    CRITICAL,
    FATAL,
    ERROR,
    WARNING,
    WARN,
    INFO,
    DEBUG,
    NOTSET,
)

__version__ = "0.0.3"

__all__ = ["Logger"]

DEFAUT_FORMAT  = "vlogging_format"
DEFAUT_FILTER  = "vlogging_filter"
DEFAUT_HANDLER = "vlogging_handler"
DEFAUT_LOGGER  = "vlogging"

class Config(object):

    DEFAUT_CONFIG = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            DEFAUT_FORMAT: formatters.getFormatConfig(formatters.SIMPLE_FORMAT),
        },
        "filters": {},
        "handlers": {
            DEFAUT_HANDLER: handlers.getConsleHandlerConfig("DEBUG", DEFAUT_FORMAT),
        },
        "loggers": {
            DEFAUT_LOGGER: loggers.getLoggerConfig("DEBUG", [DEFAUT_HANDLER]),
        },
    }

    def __init__(self):
        """Initializes the instance."""
        self.config = self.DEFAUT_CONFIG.copy()

    def configure(self, config: dict=None) -> None:
        """Configure logger settings.

        Parameters
        ----------
        config : dict, optional
            config, by default None
        """
        if config is not None:
            self.config["formatters"] = self.configureFormatters(config)
            self.config["filters"] = self.configureFilters(config)
            self.config["handlers"] = self.configureHandlers(config)
            self.config["loggers"] = self.configureLoggers(config)
        logging.config.dictConfig(self.config)

    def configureFormatters(self, config: dict) -> dict:
        """Configure formatter settings.

        Parameters
        ----------
        config : dict
            config

        Returns
        -------
        dict
            format config.
        """
        return self.configureItems(config, "formatters", DEFAUT_FORMAT)

    def configureFilters(self, config: dict) -> dict:
        """Configure filter settings.

        Parameters
        ----------
        config : dict
            config

        Returns
        -------
        dict
            filter config.
        """
        return self.configureItems(config, "filters", None)

    def configureHandlers(self, config: dict) -> dict:
        """Configure handler settings.

        Parameters
        ----------
        config : dict
            config

        Returns
        -------
        dict
            handler config.
        """
        return self.configureItems(config, "handlers", DEFAUT_HANDLER)

    def configureLoggers(self, config: dict) -> dict:
        """Configure logger settings.

        Parameters
        ----------
        config : dict
            config

        Returns
        -------
        dict
            logger config.
        """
        return self.configureItems(config, "loggers", DEFAUT_LOGGER)

    def configureItems(self, config: dict, key: str, defaut: str) -> dict:
        """Configure logger item settings.

        Parameters
        ----------
        config : dict
            config
        key : str
            config key
        defaut : str
            defaut key

        Returns
        -------
        dict
            logger item config.
        """
        result = self.configureDefautConfig(key, defaut)
        if config is None:
            cfg = {}
        else:
            cfg = config.get(key, {})

        if defaut is not None and cfg.get(defaut, None) is None:
            cfg.pop(defaut, None)

        for name in cfg:
            result[name] = cfg[name]
        return result

    def configureDefautConfig(self, key: str, defaut: str) -> dict:
        """Returns the specified default settings.

        Parameters
        ----------
        key : str
            config key
        defaut : str
            defaut key

        Returns
        -------
        dict
            defaut config.
        """
        result = {}
        if defaut is not None:
            result[defaut] = self.DEFAUT_CONFIG[key][defaut].copy()
        return result

    def prepare(self, name: str) -> None:
        """Prepare a logger with the given logger name.

        Parameters
        ----------
        name : str
            logger name
        """
        if name is None:
            return
        loggers = self.config.get("loggers")
        if name not in loggers.keys():
            loggers[name] = loggers.get("vlogging").copy()
            self.configure()


def basicConfig(**kwargs) -> None:
    """
    Do basic configuration for the logging system.

    It is a convenience method intended for use by simple scripts
    to do one-shot configuration of the logging package.

    The default behaviour is to create a StreamHandler which writes to
    sys.stderr, set a formatter using the BASIC_FORMAT format string, and
    add the handler to the root logger.

    A number of optional keyword arguments may be specified, which can alter
    the default behaviour.

    format    Use the specified format string for the handler.
    datefmt   Use the specified date/time format.
    style     If a format string is specified, use this to specify the
              type of format string (possible values '%', '{', '$', for
              %-formatting, :meth:`str.format` and :class:`string.Template`
              - defaults to '%').
    filename  Specifies that a FileHandler be created, using the specified
              filename, rather than a StreamHandler.
    filemode  Specifies the mode to open the file, if filename is specified
              (if filemode is unspecified, it defaults to 'a').
    encoding  If specified together with a filename, this encoding is passed to
              the created FileHandler, causing it to be used when the file is
              opened.
    stream    Use the specified stream to initialize the StreamHandler. Note
              that this argument is incompatible with 'filename' - if both
              are present, 'stream' is ignored.
    level     Set the logger level to the specified level.
    """
    format = kwargs.pop("format", formatters.SIMPLE_FORMAT)
    datefmt = kwargs.pop("datefmt", None)
    style = kwargs.pop("style", "%")
    formatConfig = formatters.getFormatConfig(format, datefmt, style)

    level = kwargs.pop("level", None)

    filename = kwargs.pop("filename", None)
    if filename is None:
        stream = kwargs.pop("stream", "ext://sys.stderr")
        handlerConfig = handlers.getConsleHandlerConfig(level, DEFAUT_FORMAT, stream)
    else:
        filemode = kwargs.pop("filemode", "a")
        encoding = kwargs.pop("encoding", None)
        handlerConfig = handlers.getFileHandlerConfig(filename, filemode, encoding,
                                                level, DEFAUT_FORMAT)
    loggerConfig = loggers.getLoggerConfig(level, [DEFAUT_HANDLER])

    config = {
        "formatters": {
            DEFAUT_FORMAT: formatConfig,
        },
        "handlers": {
            DEFAUT_HANDLER: handlerConfig,
        },
        "loggers": {
            DEFAUT_LOGGER: loggerConfig,
        },
    }
    _config.configure(config)


def getLogger(name: str=None, config: dict=None) -> Logger:
    """
    Return a logger with the specified name, creating it if necessary.

    If no name is specified, return the root logger.

    Parameters
    ----------
    name : str, optional
        logger name, by default None
    config : dict, optional
        Configure logging using a dictionary, by default None

    Returns
    -------
    Logger
        logger
    """
    if config is not None:
        _config.configure(config)
    if name is not None:
        _config.prepare(name)
    return logging.getLogger(name)


def critical(msg: Any, *args, **kwargs):
    """Log a message with severity 'CRITICAL' on the root logger.

    Parameters
    ----------
    msg : Any
        log message
    """
    _logger.critical(msg, *args, **kwargs)


def fatal(msg: Any, *args, **kwargs):
    """Don't use this function, use critical() instead.

    Parameters
    ----------
    msg : Any
        log message
    """
    critical(msg, *args, **kwargs)


def error(msg: Any, *args, **kwargs):
    """Log a message with severity 'ERROR' on the root logger.

    Parameters
    ----------
    msg : Any
        log message
    """
    _logger.error(msg, *args, **kwargs)


def exception(msg: Any, *args, exc_info=True, **kwargs):
    """
    Log a message with severity 'ERROR' on the root logger, with exception
    information.

    Parameters
    ----------
    msg : Any
        log message
    exc_info : bool, optional
        exception information, by default True
    """
    error(msg, *args, exc_info=exc_info, **kwargs)


def warning(msg: Any, *args, **kwargs):
    """Log a message with severity 'WARNING' on the root logger.

    Parameters
    ----------
    msg : Any
        log message
    """
    _logger.warning(msg, *args, **kwargs)


def info(msg: Any, *args, **kwargs):
    """Log a message with severity 'INFO' on the root logger.

    Parameters
    ----------
    msg : Any
        log message
    """
    _logger.info(msg, *args, **kwargs)


def debug(msg: Any, *args, **kwargs):
    """Log a message with severity 'DEBUG' on the root logger.

    Parameters
    ----------
    msg : Any
        log message
    """
    _logger.debug(msg, *args, **kwargs)


def log(level: int, msg: Any, *args, **kwargs):
    """Log 'msg % args' with the integer severity 'level' on the logger.

    Parameters
    ----------
    level : int
        log level
    msg : Any
        log message
    """
    _logger.log(level, msg, *args, **kwargs)


logging.setLoggerClass(Logger)
_config: Config = Config()
_config.configure()
_logger = getLogger(__name__)
