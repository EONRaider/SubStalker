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

import configparser
import contextlib
from configparser import ConfigParser
from pathlib import Path

from reconlib.core.base import ExternalService

from subenum.core import providers
from subenum.core.parsers.base import Parser


class ConfigurationParser(Parser):
    def __init__(self):
        super().__init__(parser=ConfigParser())

    @property
    def enumerators(self) -> set[ExternalService]:
        try:
            api_keys = {
                f"{provider}_api_key": api_key
                for provider, api_key in self.parser.items("API_KEYS")
            }
        except configparser.NoSectionError:
            return set()
        return {provider(**api_keys) for provider in providers.auth_providers}

    def parse(self, file_path: [str, Path]) -> ConfigParser:
        with contextlib.suppress(TypeError):  # Ignore non-existent paths
            self.parser.read(file_path)
        return self.parser
