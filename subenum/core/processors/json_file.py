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

import json
from collections import defaultdict
from pathlib import Path

from subenum.core.exceptions import FileReadError
from subenum.core.types.base import (
    EnumerationSubscriber,
    EnumerationPublisher,
    EnumerationResult,
)


class JSONFileOutput(EnumerationSubscriber):
    def __init__(self, subject: EnumerationPublisher, path: [str, Path]):
        """
        Output JSON-formatted subdomain enumeration results to a file

        :param subject: An instance of type EnumerationPublisher to
            subscribe to as an observer and extract results
        :param path: Absolute path to a file to which JSON-formatted
            enumeration results will be written
        """
        self.path = Path(path)
        self.results = defaultdict(dict)
        super().__init__(subject)

    def update(self, result: EnumerationResult) -> None:
        provider_response = {result.provider: [*sorted(result.subdomains)]}
        self.results[result.domain].update(provider_response)

    def _dump_results_to_file(self) -> None:
        try:
            with open(self.path, mode="a", encoding="utf_8") as file:
                json.dump(self.results, fp=file)
            self.logger.debug(
                f'File "{str(self.path)}" has been successfully opened/created for '
                f"logging of enumeration results"
            )
        except OSError as e:
            raise FileReadError(
                f"{e.__class__.__name__}: Error accessing specified file path "
                f'"{str(self.path)}"'
            )

    def cleanup(self, *args, **kwargs) -> None:
        self._dump_results_to_file()
        self.logger.info(
            f"Enumeration results successfully written in JSON format to "
            f"{str(self.path)}"
        )
        self.logger.debug(f"Logging of results was finished successfully")
