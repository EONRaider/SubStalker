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
class EnumerationResult:
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


class Logger:
    def __init__(self, name: str, level: logging = logging.DEBUG):
        """
        Set up a standard output logger with pre-configured output
        formatting

        :param name: A string representing the logger name to be
            displayed on standard output
        :param level: Minimum level to set for the logger
        """
        self.name = name
        self.level = level
        self._logging = logging.getLogger(self.name)

    def __getattr__(self, item):
        if item in self.__dict__:
            return getattr(self, item)
        return getattr(self._logging, item)

    @property
    def _logging(self) -> logging.Logger:
        return self._logger

    @_logging.setter
    def _logging(self, value: logging.Logger) -> None:
        self._logger = value
        stdout = logging.StreamHandler()
        stdout.setLevel(self.level)
        stdout.setFormatter(LogFormatter())
        self._logger.addHandler(stdout)


class EnumerationPublisher(ABC):
    def __init__(self):
        """
        Base class for all enumerators that implement the observer pattern
        """
        self._observers = []
        self._class_name = self.__class__.__name__

    @abstractmethod
    def register(self, observer) -> None:
        ...

    @abstractmethod
    def unregister(self, observer) -> None:
        ...

    @abstractmethod
    def _notify_all(self, result: EnumerationResult) -> None:
        ...


class EnumerationSubscriber(ABC):
    def __init__(self, subject: EnumerationPublisher):
        """
        Base class for all observers responsible for further processing
        and/or output of results produced by an EnumerationPublisher

        :param subject: An instance of EnumerationPublisher to observe
        """
        subject.register(self)
        self._class_name = self.__class__.__name__
        self.subject = subject
        self.logger = Logger(name=self._class_name)
        self.logger.debug(
            f"{self._class_name} observer successfully attached to instance of "
            f"{subject.__class__.__name__}"
        )

    def startup(self, *args, **kwargs) -> None:
        ...

    @abstractmethod
    def update(self, *args, **kwargs) -> None:
        ...

    def cleanup(self, *args, **kwargs) -> None:
        ...
