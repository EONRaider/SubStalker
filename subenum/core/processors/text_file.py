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
from pathlib import Path

from subenum.core.exceptions import FileReadError
from subenum.core.types import EnumResult, EnumerationPublisher, EnumerationSubscriber


class TextFileOutput(EnumerationSubscriber):
    def __init__(
        self,
        subject: EnumerationPublisher,
        path: [str, Path],
        silent_mode: bool = False,
    ):
        """
        Output line-separated subdomain enumeration results to a file

        :param subject: An instance of type EnumerationPublisher to
            subscribe to as an observer and extract results
        :param path: Absolute path to a file to which enumeration
            results will be written
        :param silent_mode: Boolean that sets the level of verbosity of
            output messages. Set to False by default to display
            information such as the number of found domains and the
            total time taken by the operation.
        """
        self.path = Path(path)
        self._fd = None
        super().__init__(
            subject, silent_mode, logger=logging.getLogger("TextFileOutput")
        )

    def startup(self, *args, **kwargs) -> None:
        try:
            """Opening, writing and closing of the file descriptor are
            split between, respectively, startup, update and cleanup, in
            order to ensure that a single file descriptor is used
            throughout the entire lifetime of a single TextFileOutput
            object, preventing unnecessary system calls each time a
            write operation takes place"""
            self._fd = self.path.open(mode="a", encoding="utf_8")
        except OSError as e:
            raise FileReadError(
                f"{e.__class__.__name__}: Error accessing specified file path "
                f'"{str(self.path)}"'
            )

    def update(self, result: EnumResult) -> None:
        for domain in sorted(result.subdomains):
            # Write only de-duplicated results to file
            if domain not in self.subject.found_domains[result.domain]:
                self._fd.write(f"{domain}\n")

    def cleanup(self, *args, **kwargs) -> None:
        self._fd.close()
        self.logger.info(
            f"Enumeration results successfully written in text format to "
            f"{self._fd.name}"
        )
