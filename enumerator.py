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
from subenum.core.types.base import EnumerationPublisher
from subenum.enumerators.passive import PassiveEnumerator


class App:
    def __init__(self, *, cli_parser: CLIParser, config_parser: ConfigurationParser):
        self.cli_parser = cli_parser
        self.config_parser = config_parser
        # Set the minimum global level for all loggers
        logging.getLogger().setLevel(self.logger_level)

    @property
    def cli_parser(self) -> CLIParser:
        return self._cli_parser

    @cli_parser.setter
    def cli_parser(self, parser: CLIParser):
        self._cli_parser = parser
        self._cli_args = parser.parse()

    @property
    def config_parser(self) -> ConfigurationParser:
        return self._config_parser

    @config_parser.setter
    def config_parser(self, parser: ConfigurationParser):
        self._config_parser = parser
        self._config_args = parser.parse(file_path=self._cli_args.config_file)

    @property
    def logger_level(self) -> logging:
        """
        Set the logging level based on user-defined verbosity settings
        """
        if self._cli_args.debug:
            return logging.DEBUG
        elif self._cli_args.silent:
            return logging.WARNING
        else:
            return logging.INFO

    def _attach_observers(self, subject: EnumerationPublisher) -> None:
        """
        Instantiate all observers selected for output/processing of
        subdomain enumeration results
        """
        ScreenOutput(subject)
        if self._cli_args.output is not None:
            TextFileOutput(subject, path=self._cli_args.output)
        if self._cli_args.json is not None:
            JSONFileOutput(subject, path=self._cli_args.json)

    def run(self) -> None:
        passive_enum = PassiveEnumerator(
            targets=self._cli_args.targets,
            providers=self.cli_parser.providers | self.config_parser.providers,
            max_threads=self._cli_args.max_threads,
            retry_time=self._cli_args.retry,
            max_retries=self._cli_args.max_retries,
        )

        self._attach_observers(passive_enum)

        try:
            with passive_enum as enumerator:
                for result in enumerator.execute():
                    if isinstance(result, EnumeratorException):
                        raise result
        except KeyboardInterrupt:
            raise SystemExit("[!] Subdomain enumeration aborted by user. Exiting...")


if __name__ == "__main__":
    app = App(cli_parser=CLIParser(), config_parser=ConfigurationParser())
    app.run()
