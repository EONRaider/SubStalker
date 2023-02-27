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

from substalker.core.parsers.configuration import ConfigurationParser


class TestConfigurationParser:
    def test_parse_config(self, config_file):
        """
        GIVEN a valid path to a correctly formatted configuration file
        WHEN this file contains a sample item representing a data
            provider called "virustotal"
        THEN the value mapped to this item must be returned by the parser
            without exceptions
        """
        config = ConfigurationParser()
        config.parse(file_path=config_file)
        assert (
            config.parser["API_KEYS"]["virustotal"] == "Test-VirusTotal-API-Key-12345"
        )

    def test_parse_invalid_config(self):
        """
        GIVEN a path to a configuration file
        WHEN this path is invalid
        THEN the parser's "providers" attribute must be an empty set
        """
        config = ConfigurationParser()
        config.parse(file_path=None)
        assert config.providers == set()

    def test_parse_invalid_provider(self, config_file):
        """
        GIVEN a valid path to a correctly formatted configuration file
        WHEN this file contains a sample item representing an unknown
            data provider
        THEN the unknown provider must be ignored but all known providers
            must be returned as elements of the parser's "providers"
            attribute
        """
        config = ConfigurationParser()
        config.parse(file_path=config_file)
        config.parser["API_KEYS"]["unknown_provider"] = "Some-API-Key"
        assert len(config.providers) == 1
