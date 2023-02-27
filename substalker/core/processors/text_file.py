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

from pathlib import Path

from substalker.core.exceptions import FileReadError
from substalker.core.types.base import (
    EnumerationResult,
    EnumerationPublisher,
    EnumerationSubscriber,
)


class TextFileOutput(EnumerationSubscriber):
    def __init__(self, subject: EnumerationPublisher, path: [str, Path]):
        """
        Output line-separated subdomain enumeration results to a file

        :param subject: An instance of type EnumerationPublisher to
            subscribe to as an observer and extract results
        :param path: Absolute path to a file to which enumeration
            results will be written
        """
        self.path = Path(path)
        self._fd = None
        super().__init__(subject)

    def startup(self, *args, **kwargs) -> None:
        try:
            """Opening, writing and closing of the file descriptor are
            split between, respectively, startup, update and cleanup, in
            order to ensure that a single file descriptor is used
            throughout the entire lifetime of a single TextFileOutput
            object, preventing unnecessary system calls every time a
            write operation takes place"""
            self._fd = self.path.open(mode="a", encoding="utf_8")
            self.logger.debug(
                f'File "{self._fd.name}" has been successfully opened/created for '
                f"logging of enumeration results"
            )
        except OSError as e:
            raise FileReadError(
                f"{e.__class__.__name__}: Error accessing specified file path "
                f'"{str(self.path)}"'
            )

    def update(self, result: EnumerationResult) -> None:
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
        self.logger.debug(f"Logging of results was finished successfully")