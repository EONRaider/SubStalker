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
from pathlib import Path

from reconlib import CRTShAPI, HackerTargetAPI, VirusTotalAPI

from subenum.output import EnumeratorSubscriber


class Enumerator:
    def __init__(
        self, targets: Collection[str], *, output_file: [str, Path], max_threads: int
    ):
        self.targets: Collection[str] = targets
        self.output_file: [str, Path] = output_file
        self.max_threads: int = max_threads
        self._observers: list[EnumeratorSubscriber] = []

    def register(self, observer: EnumeratorSubscriber) -> None:
        self._observers.append(observer)

    def _notify_all(self, result) -> None:
        [observer.update(result) for observer in self._observers]

    @staticmethod
    def query_api(domain) -> set[str]:
        apis = CRTShAPI(), HackerTargetAPI(), VirusTotalAPI()
        return set().union(*(api.fetch_subdomains(target=domain) for api in apis))

    def execute(self) -> None:
        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            try:
                for result in executor.map(self.query_api, self.targets):
                    self._notify_all(result)
            except KeyboardInterrupt:
                print("[!] Subdomain enumeration terminated by user. Exiting...")

        for observer in self._observers:
            observer.end_output()
