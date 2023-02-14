"""
SubdomainEnumerator: Find subdomains belonging to given target hosts
using active and passive enumeration methods

Author: EONRaider
GitHub: https://github.com/EONRaider
Contact: https://www.twitter.com/eon_raider
    Copyright (C) 2023 EONRaider @ keybase.io/eonraider
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program. If not, see
    <https://github.com/EONRaider/SubdomainEnumerator/blob/master/LICENSE>.
"""

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class EnumResult:
    """
    Representation of a subdomain enumeration result
    """

    provider: str
    domain: str
    subdomains: set[str]


class LogFormatter(logging.Formatter):
    grey = "\x1b[2m"
    yellow = "\x1b[93m"
    red = "\x1b[91m"
    green = "\x1b[92m"
    blue = "\x1b[94m"
    reset = "\x1b[0m"

    FORMATS = {
        logging.DEBUG: f"{blue}[%(levelname)s] - %(name)s - %(asctime)s - %(message)s"
        f"{reset}",
        logging.INFO: f"{grey}[{yellow}%(levelname)s{reset}{grey}] %(message)s{reset}",
        logging.WARNING: f"{grey}%(message)s{reset}",
    }

    def format(self, record: logging.LogRecord) -> str:
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


class EnumerationPublisher(ABC):
    def __init__(self):
        """
        Base class for all enumerators that implement the observer pattern
        """
        self._observers = []

    @abstractmethod
    def register(self, observer) -> None:
        ...

    @abstractmethod
    def unregister(self, observer) -> None:
        ...

    @abstractmethod
    def _notify_all(self, result: EnumResult) -> None:
        ...


class EnumerationSubscriber(ABC):
    def __init__(
        self,
        subject: EnumerationPublisher,
        silent_mode: bool,
        *,
        logger: logging.Logger,
        debug: bool,
    ):
        """
        Base class for all observers responsible for further processing
        and/or output of results produced by an EnumerationPublisher

        :param subject: An instance of EnumerationPublisher to observe
        :param silent_mode: Boolean that sets the level of verbosity of
            output messages. Set to False by default to display
            information such as the number of found domains and the
            total time taken by the operation, among others.
        :param logger: Instance of Logger that will be used for
            displaying status messages
        :param debug: Allow displaying of debug messages. Overrides the
            value set by "silent_mode".
        """
        subject.register(self)
        self.subject = subject
        self.silent = silent_mode
        self.logger = logger
        self.debug = debug
        self._add_logging_handlers()
        self.logger.debug(
            f"{self.__class__.__name__} observer successfully attached to instance of "
            f"{subject.__class__.__name__}"
        )

    def _add_logging_handlers(self) -> None:
        """
        Set up StreamHandler loggers and add them to the main logger
        """
        stdout = logging.StreamHandler()

        if self.debug:
            level = logging.DEBUG
        elif self.silent:
            """Messages logged on "startup" and "cleanup" must use the
            INFO level, so they will be suppressed if "silent" is True
            (since WARNING stands at a higher level)"""
            level = logging.WARNING
        else:
            level = logging.INFO

        stdout.setLevel(level)
        stdout.setFormatter(LogFormatter())
        self.logger.addHandler(stdout)

    def startup(self, *args, **kwargs) -> None:
        ...

    @abstractmethod
    def update(self, *args, **kwargs) -> None:
        ...

    def cleanup(self, *args, **kwargs) -> None:
        ...
