import logging
from typing import Optional


class CustomLoggerAdapter(logging.LoggerAdapter):
    """
    A custom logger adapter that adds support for additional fields in log messages.

    Parameters
    ----------
    name : str
        The name of the logger to be used.
    kwargs : dict, optional
        Additional keyword arguments to be passed to the logger.
    level : str, optional
        The logging level to be used. Defaults to "DEBUG".
    formatter : logging.Formatter, optional
        The formatter to be used for log messages. Defaults to a basic formatter.

    Attributes
    ----------
    formatter : logging.Formatter
        The formatter to be used for log messages.
    logger : logging.Logger
        The logger to be used.
    default_handler : logging.StreamHandler
        The default handler for log messages.

    Methods
    -------
    process(msg, kwargs)
        Add the event, service, and tag fields to the log message.

    Examples
    --------
    >>> from ailab_utils.logger import CustomLoggerAdapter
    >>> logger = CustomLoggerAdapter("test_logger", level ="DEBUG", {"service": "test_service"})
    >>> logger.debug("test message")
    >>> logger.info("test message", **{"event": "test_event", "tag": "test_tag"}})
    ... timestamp [INFO] test_logger test_service - test_event - test_tag - test message
    >>> logger.warning("test message")
    """

    def __init__(
        self,
        name: str,
        kwargs: Optional[dict] = None,
        level: str = "DEBUG",
        formatter: Optional[logging.Formatter] = None,
    ) -> None:
        """
        Initialize the CustomLoggerAdapter class.

        Parameters
        ----------
        name : str
            The name of the logger to be used.
        kwargs : dict, optional
            Additional keyword arguments to be passed to the logger.
        level : str, optional
            The logging level to be used. Defaults to "DEBUG".
        formatter : logging.Formatter, optional
            The formatter to be used for log messages. Defaults to a basic formatter.

        Returns
        -------
        None

        """
        self.formatter = formatter
        if kwargs is None:
            kwargs = {}

        logging.basicConfig(level=level.upper())

        self.logger = logging.getLogger(name)
        self.default_handler = logging.StreamHandler()

        if self.formatter is None:
            self.formatter = logging.Formatter(
                "%(asctime)s [%(levelname)s] %(module)s %(message)s"
            )

        self.default_handler.setFormatter(self.formatter)

        self.logger.addHandler(self.default_handler)
        self.logger.propagate = False
        super().__init__(self.logger, kwargs)

    def process(self, msg, kwargs):
        """
        Add the event, service, and tag fields to the log message.

        Parameters
        ----------
        msg : str
            The log message to be processed.
        kwargs : dict
            Additional keyword arguments to be passed to the logger.

        Returns
        -------
        str
            The processed log message.

        """
        event = kwargs.pop("event", self.extra.get("event"))
        service = kwargs.pop("service", self.extra.get("service"))
        tag = kwargs.pop("tag", self.extra.get("tag"))
        # add each field to the log message if it is not empty
        if tag:
            msg = f"{tag} - {msg}"
        if event:
            msg = f"{event} - {msg}"
        if service:
            msg = f"{service} - {msg}"

        return msg, kwargs
