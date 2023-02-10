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
    def __init__(self, subject: EnumerationPublisher):
        """
        Base class for all observers responsible for further processing
        and/or output of results produced by an EnumerationPublisher

        :param subject: An instance of EnumerationPublisher to observe
        """
        subject.register(self)
        self.subject = subject

    def startup(self, *args, **kwargs) -> None:
        ...

    @abstractmethod
    def update(self, *args, **kwargs) -> None:
        ...

    def cleanup(self, *args, **kwargs) -> None:
        ...
