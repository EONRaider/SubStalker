"""
SubStalker: Find subdomains belonging to given target hosts
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
    <https://github.com/EONRaider/SubStalker/blob/master/LICENSE>.
"""

import concurrent.futures
import time
import urllib.error
from collections import defaultdict
from collections.abc import Collection, Iterator
from contextlib import suppress

from reconlib.core.base import ExternalService

from substalker.core.types.base import (
    EnumerationResult,
    EnumerationPublisher,
    EnumerationSubscriber,
)
from substalker.core.types.log import Logger


class PassiveSubdomainEnumerator(EnumerationPublisher):
    def __init__(
        self,
        targets: Collection[str],
        *,
        providers: Collection[ExternalService],
        max_threads: int,
        retry_time: int,
        max_retries: int,
    ):
        """
        Enumerate subdomains of given targets by using available data
        providers

        :param targets: A collection of strings defining target domains
        :param providers: A collection of instances of ExternalService
            to be queried during the enumeration of subdomains of
            selected targets
        :param max_threads: Maximum number of threads to use when
            enumerating subdomains. A new thread will be spawned for
            each combination of data provider and target domain
        :param retry_time: Time to wait before attempting a new request
            to a data provider whose usage quota has been exceeded
        :param max_retries: Maximum number of times the application
            should retry fetching results from any given data provider
            whenever error responses are returned from it
        """
        super().__init__()
        self.targets: Collection[str] = targets
        self.providers: Collection[ExternalService] = providers
        self.max_threads: int = max_threads
        self.retry_time: int = retry_time
        self.max_retries = max_retries
        self.found_domains = defaultdict(set)
        self.logger = Logger(name=self._class_name)

    def __enter__(self) -> "PassiveSubdomainEnumerator":
        self.start_time = time.perf_counter()
        [observer.startup(subject=self) for observer in self._observers]
        return self

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

        :param result: An instance of type EnumerationResult
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
        :return: An instance of type EnumerationResult
        """
        for attempt in range(1, self.max_retries + 1):
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
            except urllib.error.HTTPError as e:
                self.logger.error(
                    f'Received "{e.reason}" error message with code {e.code} from '
                    f"{provider.service_name}! Retrying in {self.retry_time} seconds "
                    f"(attempt {attempt}/{self.max_retries})..."
                )
                time.sleep(self.retry_time)
        self.logger.error(
            f"Could not fetch subdomain enumeration results from "
            f"{provider.service_name} after {self.max_retries} failed attempts. "
            f"Continuing..."
        )

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
                    self._notify_all(result)
                    self.found_domains[result.domain] |= result.subdomains
                    yield result
        self.logger.debug("Subdomain enumeration finished")
