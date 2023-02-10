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

from pathlib import Path

from subenum.core.exceptions import FileReadError
from subenum.core.types import EnumResult, EnumerationPublisher, EnumerationSubscriber


class FileOutput(EnumerationSubscriber):
    def __init__(self, subject: EnumerationPublisher, path: [str, Path]):
        """
        Output subdomain enumeration results to a file with a specified
        path

        :param subject: An instance of type EnumerationPublisher to
            subscribe to as an observer and extract results
        :param path: Absolute path to a file to which enumeration
            results will be written
        """
        super().__init__(subject)
        self.path = Path(path)
        self.fd = None

    def startup(self, *args, **kwargs) -> None:
        try:
            self.fd = self.path.open(mode="a", encoding="utf_8")
        except OSError as e:
            raise FileReadError(
                f"{e.__class__.__name__}: Error accessing specified file path "
                f'"{str(self.path)}"'
            )

    def update(self, result: EnumResult) -> None:
        self._known_domains |= (new_domains := self._get_new_domains(result))
        [self.fd.write(f"{domain}\n") for domain in sorted(new_domains)]

    def cleanup(self, *args, **kwargs) -> None:
        self.fd.close()
        print(f"[+] Enumeration results successfully written to {self.fd.name}")
