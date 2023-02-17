#!/usr/bin/python3

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

from subenum.core.exceptions import EnumeratorException
from subenum.core.parsers.cli import CLIParser
from subenum.core.parsers.configuration import ConfigurationParser
from subenum.core.processors.json_file import JSONFileOutput
from subenum.core.processors.text_file import TextFileOutput
from subenum.core.processors.screen import ScreenOutput
from subenum.enumerator import Enumerator


class App:
    def __init__(self):
        self.cli_args = (cli_parser := CLIParser()).parse()
        (config_parser := ConfigurationParser()).parse(
            file_path=self.cli_args.config_file
        )

        # Set the minimum global level for all loggers
        logging.getLogger().setLevel(self.logger_level)

        self.enumerator = Enumerator(
            targets=self.cli_args.targets,
            providers=cli_parser.providers | config_parser.providers,
            max_threads=self.cli_args.max_threads,
            retry_time=self.cli_args.retry,
            max_retries=self.cli_args.max_retries,
        )

    @property
    def logger_level(self) -> logging:
        """
        Set the logging level based on user-defined verbosity settings
        """
        if self.cli_args.debug:
            return logging.DEBUG
        elif self.cli_args.silent:
            return logging.WARNING
        else:
            return logging.INFO

    def _attach_observers(self) -> None:
        """
        Instantiate all observers selected for output/processing of
        subdomain enumeration results
        """
        ScreenOutput(subject=self.enumerator)
        if self.cli_args.output is not None:
            TextFileOutput(subject=self.enumerator, path=self.cli_args.output)
        if self.cli_args.json is not None:
            JSONFileOutput(subject=self.enumerator, path=self.cli_args.json)

    def run(self) -> None:
        self._attach_observers()
        try:
            with self.enumerator:
                for result in self.enumerator.execute():
                    if isinstance(result, EnumeratorException):
                        raise result
        except KeyboardInterrupt:
            raise SystemExit("[!] Subdomain enumeration aborted by user. Exiting...")


if __name__ == "__main__":
    App().run()
