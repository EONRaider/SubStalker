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
from pathlib import Path

from subenum.core.exceptions import EnumeratorException
from subenum.core.parsers.cli import CLIParser
from subenum.core.parsers.configuration import ConfigurationParser
from subenum.core.processors.json_file import JSONFileOutput
from subenum.core.processors.text_file import TextFileOutput
from subenum.core.processors.screen import ScreenOutput
from subenum.core.scheduler import Scheduler
from subenum.core.types.base import EnumerationPublisher
from subenum.core.enumerators.passive import PassiveSubdomainEnumerator


class SubdomainEnumerator:
    def __init__(
        self,
        *,
        file_path: [str, Path] = None,
        json_path: [str, Path] = None,
    ):
        self.file_path = file_path
        self.json_path = json_path
        self.modules: list[EnumerationPublisher] = []

    def attach_enumeration_module(self, module: EnumerationPublisher) -> None:
        """
        Attach new modules to the Enumerator and initialize their
        observers

        :param module: An instance of a type that implements the
            EnumerationPublisher interface
        """
        self.modules.append(module)
        self._attach_observers(module)

    def _attach_observers(self, subject: EnumerationPublisher) -> None:
        """
        Instantiate all observers selected for output/processing of
        subdomain enumeration results
        """
        ScreenOutput(subject)
        if self.file_path is not None:
            TextFileOutput(subject, path=self.file_path)
        if self.json_path is not None:
            JSONFileOutput(subject, path=self.json_path)

    def execute(self) -> None:
        for module in self.modules:
            with module:
                for result in module.execute():
                    if isinstance(result, EnumeratorException):
                        raise result


if __name__ == "__main__":
    cli_args = (cli_parser := CLIParser()).parse()
    (config_parser := ConfigurationParser()).parse(file_path=cli_args.config_file)
    logging.getLogger().setLevel(cli_parser.args.logger_level)

    enumerator = SubdomainEnumerator(
        file_path=cli_args.output,
        json_path=cli_args.json,
    )

    enumerator.attach_enumeration_module(
        PassiveSubdomainEnumerator(
            targets=cli_args.targets,
            providers=cli_parser.providers | config_parser.providers,
            max_threads=cli_args.max_threads,
            retry_time=cli_args.retry,
            max_retries=cli_args.max_retries,
        )
    )

    try:
        Scheduler(task=enumerator.execute, interval=cli_args.interval).execute()
    except KeyboardInterrupt:
        raise SystemExit("[!] Subdomain enumeration aborted by user. Exiting...")
