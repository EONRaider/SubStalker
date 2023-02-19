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

import contextlib
from configparser import ConfigParser, NoSectionError
from pathlib import Path

from reconlib.core.base import ExternalService

from subenum.core import providers
from subenum.core.parsers.base import Parser


class ConfigurationParser(Parser):
    def __init__(self):
        """
        Parser of INI-formatted configuration files for the application
        """
        super().__init__(parser=ConfigParser())

    @property
    def providers(self) -> set[ExternalService]:
        """
        Get instances of data providers specified by the sections of a
        INI configuration file
        :return: A set of instances of non-authenticated data providers
            of type ExternalService as defined by the INI configuration
            file
        """
        try:
            # Return all providers specified in the file
            auth_data = {
                f"{provider}_auth": auth_value
                for provider, auth_value in self.parser.items("API_KEYS")
            }
        except NoSectionError:
            # Return an empty set if no authentication data was provided
            return set()
        """Return all available authenticated data providers if the 
        specification of their authentication data was found in the
        INI configuration file"""
        return {provider(**auth_data) for provider in providers.auth_providers}

    def parse(self, file_path: [str, Path]) -> ConfigParser:
        with contextlib.suppress(TypeError):  # Ignore non-existent paths
            self.parser.read(file_path)
        return self.parser
