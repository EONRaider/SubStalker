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

from subenum.core.types import EnumResult, EnumerationPublisher, EnumerationSubscriber


class ScreenOutput(EnumerationSubscriber):
    def __init__(
        self,
        subject: EnumerationPublisher,
        *,
        silent_mode: bool = False,
        debug: bool = False,
    ):
        """
        Output subdomain enumeration results on STDOUT

        :param subject: An instance of type EnumerationPublisher to
            subscribe to as an observer and extract results
        :param silent_mode: Boolean that sets the level of verbosity of
            output messages. Set to False by default to display
            information such as the number of found domains and the
            total time taken by the operation, among others.
        :param debug: Allow displaying of debug messages. Overrides the
            value set by "silent_mode".
        """
        super().__init__(subject, silent_mode=silent_mode, debug=debug)

    def startup(self, subject: EnumerationPublisher) -> None:
        self.logger.info(
            f"Subdomain enumerator started with {subject.max_threads} threads for "
            f"{' | '.join(subject.targets)}",
        )

    def update(self, result: EnumResult) -> None:
        self.logger.debug(f"{self._class_name} logging results from {result.provider}")
        for domain in sorted(result.subdomains):
            # Display only de-duplicated results on STDOUT
            if domain not in self.subject.found_domains[result.domain]:
                self.logger.warning(
                    f"{domain}" if self.silent else f"\t[{result.provider}] {domain}"
                )

    def cleanup(self, *args, **kwargs) -> None:
        self.logger.info(
            f"Enumeration of {(num_domains := len(self.subject.targets))} "
            f"{'domain' if num_domains == 1 else 'domains'} was completed in "
            f"{self.subject.total_time:.2f} seconds and found "
            f"{self.subject.num_found_domains} subdomains"
        )
        self.logger.debug(
            f"Logging of results by {self._class_name} observer was finished "
            f"successfully"
        )
