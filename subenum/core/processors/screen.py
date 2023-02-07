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

from subenum.core.types import EnumResult
from subenum.core.processors.base import EnumerationPublisher, EnumerationSubscriber


class ScreenOutput(EnumerationSubscriber):
    def __init__(self, subject: EnumerationPublisher):
        super().__init__(subject)

    def startup(self, subject: EnumerationPublisher) -> None:
        print(
            f"[+] Subdomain enumerator started with {subject.max_threads} threads "
            f"for {' | '.join(subject.targets)}",
            end="\n",
        )

    def update(self, result: EnumResult) -> None:
        self._known_domains |= (new_domains := self._get_new_domains(result))
        [print(f"\t{domain}") for domain in sorted(new_domains)]

    def cleanup(self, *args, **kwargs) -> None:
        print(
            f"[+] Enumeration of {len(self.subject.targets)} domains completed in "
            f"{self.subject.total_time:.2f} seconds"
        )
