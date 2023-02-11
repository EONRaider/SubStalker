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


class CustomFormatter(logging.Formatter):
    grey = "\x1b[2m"
    yellow = "\x1b[93m"
    red = "\x1b[91m"
    green = "\x1b[92m"
    reset = "\x1b[0m"

    FORMATS = {
        logging.DEBUG: f"{red}[%(levelname)s] - %(name)s - %(asctime)s - %(message)s"
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
        self, subject: EnumerationPublisher, silent_mode: bool, logger: logging.Logger
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
        """
        subject.register(self)
        self.silent = silent_mode
        self.subject = subject
        self.logger = logger
        self._add_logging_handlers()

    def _add_logging_handlers(self) -> None:
        """
        Set up StreamHandler loggers and add them to the main logger
        """
        stdout = logging.StreamHandler()

        """Messages logged on "startup" and "cleanup" use the INFO level,
        so they will be suppressed if "silent" is True (since WARNING 
        stands at a higher level)"""
        stdout.setLevel(logging.WARNING if self.silent else logging.INFO)

        stdout.setFormatter(CustomFormatter())
        self.logger.addHandler(stdout)

    def startup(self, *args, **kwargs) -> None:
        ...

    @abstractmethod
    def update(self, *args, **kwargs) -> None:
        ...

    def cleanup(self, *args, **kwargs) -> None:
        ...
