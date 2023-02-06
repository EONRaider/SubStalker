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

from collections.abc import Collection
from concurrent.futures import ThreadPoolExecutor
from contextlib import suppress
from pathlib import Path

from reconlib.core.base import ExternalService

from subenum.core.types import EnumerationPublisher, EnumerationSubscriber


class Enumerator(EnumerationPublisher):
    def __init__(
        self,
        targets: Collection[str],
        *,
        enumerators: Collection[ExternalService],
        max_threads: int,
        output_file: [str, Path] = None
    ):
        super().__init__()
        self.targets: Collection[str] = targets
        self.enumerators: Collection[ExternalService] = enumerators
        self.output_file: [str, Path] = output_file
        self.max_threads: int = max_threads

    @property
    def tasks(self) -> tuple:
        return tuple(
            (target, api) for target in self.targets for api in self.enumerators
        )

    def register(self, observer: EnumerationSubscriber) -> None:
        """
        Attach an observer to the enumerator for further processing
        and/or output of results.

        :param observer: An object implementing the interface of
            EnumerationSubscriber
        """
        self._observers.append(observer)

    def unregister(self, observer: EnumerationSubscriber) -> None:
        """
        Remove an observer previously attached to the enumerator.

        :param observer: An object implementing the interface of
            EnumerationSubscriber
        """
        with suppress(ValueError):
            # Supress exceptions raised by an attempt to unregister a
            # non-existent observer
            self._observers.remove(observer)

    def _notify_all(self, result: set[str]) -> None:
        """
        Notify all registered observers of an enumeration result for
        further processing and/or output.
        :param result: A set of strings representing enumerated
            subdomains
        """
        [observer.update(result) for observer in self._observers]

    @staticmethod
    def query_api(target: str, api: ExternalService) -> set[str]:
        return api.fetch_subdomains(target)

    def execute(self) -> None:
        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            try:
                for result in executor.map(
                    lambda task: self.query_api(*task), self.tasks
                ):
                    self._notify_all(result)
            except KeyboardInterrupt:
                print("[!] Subdomain enumeration terminated by user. Exiting...")

        for observer in self._observers:
            observer.end_output()
