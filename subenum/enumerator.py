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

import concurrent.futures
import time
from collections import defaultdict
from collections.abc import Collection, Iterator
from contextlib import suppress

import reconlib
from reconlib.core.base import ExternalService

from subenum.core.types import (
    EnumerationResult,
    EnumerationPublisher,
    EnumerationSubscriber,
    Logger,
)


class Enumerator(EnumerationPublisher):
    def __init__(
        self,
        targets: Collection[str],
        *,
        providers: Collection[ExternalService],
        max_threads: int,
        retry_time: int,
    ):
        """
        Enumerate subdomains of given targets by using available data
        providers

        :param targets: A collection of strings defining target domains
        :param providers: A collection of instances of ExternalServices
            to be queried during the enumeration of subdomains of
            selected targets
        :param max_threads: Maximum number of threads to use when
            enumerating subdomains. A new thread will be spawned for
            each combination of data provider and target domain
        :param retry_time: Time to wait before attempting a new request
            to a data provider whose usage quota has been exceeded
        """
        super().__init__()
        self.targets: Collection[str] = targets
        self.providers: Collection[ExternalService] = providers
        self.max_threads: int = max_threads
        self.retry_time: int = retry_time
        self.found_domains = defaultdict(set)
        self.logger = Logger(name=self._class_name)

    def __enter__(self) -> None:
        self.start_time = time.perf_counter()
        [observer.startup(subject=self) for observer in self._observers]

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.total_time = time.perf_counter() - self.start_time
        [observer.cleanup(subject=self) for observer in self._observers]

    @property
    def num_found_domains(self) -> int:
        """
        Get the total number of subdomains found for all targets and
        from all data providers
        """
        return sum(len(subdomains) for subdomains in self.found_domains.values())

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

    def _notify_all(self, result: EnumerationResult) -> None:
        """
        Notify all registered observers of an enumeration result for
        further processing and/or output.

        :param result: An instance of type EnumResult
        """
        [observer.update(result) for observer in self._observers]

    def query_provider(
        self, provider: ExternalService, target: str
    ) -> EnumerationResult:
        """
        Query a data provider about known subdomains of a given target
        domain

        :param provider: An instance of type ExternalService to query
        :param target: A string defining a target domain
        :return: An instance of type EnumResult containing enumeration
            results as its attributes
        """
        while True:
            try:
                self.logger.debug(
                    f"Querying subdomain information for {target} from "
                    f"{provider.service_name}"
                )
                return EnumerationResult(
                    provider=provider.service_name,
                    domain=target,
                    subdomains=provider.fetch_subdomains(target),
                )
            except reconlib.core.exceptions.APIQuotaUsageError:
                self.logger.debug(
                    f"Received HTTP response code 403 from {provider.service_name}! "
                    f"Retrying in {self.retry_time} seconds..."
                )
                time.sleep(self.retry_time)

    def execute(self) -> Iterator[EnumerationResult]:
        self.logger.debug("Subdomain enumeration started")
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_threads) as ex:
            """Generate tuples containing combinations of available
            providers and targets to pass as tasks to spawned threads"""
            tasks: Iterator[tuple[ExternalService, str]] = (
                (provider, target)
                for target in self.targets
                for provider in self.providers
            )
            queries = {ex.submit(self.query_provider, *task): task for task in tasks}

            for future in concurrent.futures.as_completed(queries):
                if result := future.result():
                    """Add results generated by the enumeration of a given
                    target to "found_domains", notify all observers, if any,
                    of newly found results, and yield them"""
                    self._notify_all(result)
                    self.found_domains[result.domain] |= result.subdomains
                    yield result
        self.logger.debug("Subdomain enumeration finished")
