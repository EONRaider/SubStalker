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

import argparse
import importlib.metadata
import re
import sys
from collections.abc import Iterator

from reconlib.core.base import ExternalService

from subenum.core import providers
from subenum.core.exceptions import (
    TargetSpecificationError,
    FileReadError,
    InvalidProviderError,
)
from subenum.core.parsers.base import Parser


class CLIParser(Parser):
    max_threads = 10

    def __init__(self):
        """
        Parser of Command Line Interface options for the application
        """
        super().__init__(
            parser=argparse.ArgumentParser(
                formatter_class=argparse.RawDescriptionHelpFormatter,
                description="Find subdomains belonging to given target hosts using "
                "active and passive enumeration methods",
            )
        )
        self.targeting = self.parser.add_mutually_exclusive_group(required=True)
        self.args = None

    @property
    def providers(self) -> set[ExternalService]:
        """
        Get instances of data providers specified by a CLI option

        :return: A set of instances of non-authenticated data providers
            of type ExternalService as defined by the CLI parser
        """
        if self.args.providers is not None:
            # Return all providers specified through the CLI
            user_options = self._read_from_cli_option(self.args.providers)
            try:
                return {getattr(providers, api)() for api in user_options}
            except AttributeError:
                raise InvalidProviderError(
                    "Unknown provider name was supplied as a CLI option. Cannot "
                    "proceed."
                )
        """Return all available non-authenticated data providers if
        no specification was made through the CLI"""
        return {provider() for provider in providers.open_providers}

    def parse(self, *args, **kwargs) -> argparse.Namespace:
        self.targeting.add_argument(
            "-t",
            "--targets",
            type=str,
            help="A sequence of one or more comma-separated domain names to enumerate",
        )
        self.targeting.add_argument(
            "-f",
            "--from-file",
            type=str,
            help="Absolute path to a file containing line-separated domain names to "
            "enumerate",
        )
        self.targeting.add_argument(
            "--stdin",
            action="store_true",
            help="Input line-separated domain names directly from STDIN. Useful for "
            "piping directly from the output of another application or the redirected "
            "output of a file.",
        )
        self.targeting.add_argument(
            "--version",
            action="store_true",
            help="Display the version of SubdomainEnumerator",
        )
        self.parser.add_argument(
            "-p",
            "--providers",
            type=str,
            help="A comma-separated list of external services to use when fetching "
            "subdomains. Uses all open data providers that do not require an API key "
            "for access by default. Check the online documentation for available "
            "services.",
        )
        self.parser.add_argument(
            "-o",
            "--output",
            type=str,
            help="Absolute path of a file to which enumeration results will be written "
            "in line-separated text format",
        )
        self.parser.add_argument(
            "-j",
            "--json",
            type=str,
            help="Absolute path of a file to which enumeration results will be written "
            "in JSON format",
        )
        self.parser.add_argument(
            "--silent",
            action="store_true",
            help="Suppress helper output from STDOUT. Only enumerated subdomains will "
            "be shown. Useful for piping the output into another application or "
            "redirecting to a file.",
        )
        self.parser.add_argument(
            "--max-threads",
            type=int,
            help=f"Maximum number of threads to use when enumerating subdomains "
            f"(defaults to {self.max_threads})",
            default=self.max_threads,
        )
        self.parser.add_argument(
            "--config-file",
            type=str,
            help="Absolute path to an INI file containing the API keys to "
            "authenticated external services to be queried by the application, if any",
        )
        self.parser.add_argument(
            "--debug", action="store_true", help="Display debugging messages on STDOUT"
        )
        self.args = self.parser.parse_args(*args, **kwargs)

        if self.args.version:
            raise SystemExit(importlib.metadata.version("subenum"))

        self.args.targets = self._set_targets()
        return self.args

    @staticmethod
    def _read_from_stdin() -> Iterator[str]:
        """
        Read strings passed in from standard input

        :return: An iterator of line-separated strings from STDIN
        """
        yield from (line.strip() for line in sys.stdin.readlines())

    def _read_from_file(self) -> Iterator[str]:
        """
        Read strings from a file

        :return: An iterator of line-separated strings from a file
        """
        try:
            with open(self.args.from_file, encoding="utf_8") as file:
                yield from (line.strip() for line in file.readlines())
        except OSError as e:
            raise FileReadError(
                f"{e.__class__.__name__}: Failed to read target specification from "
                f'file "{str(self.args.from_file)}"'
            )

    @staticmethod
    def _read_from_cli_option(option: str) -> Iterator[str]:
        """
        Read strings derived from a single string captured by the CLI
        parser

        :param option: A string containing comma-separated domain names
            to target
        """
        yield from re.split(r"\s*,\s*", option)

    def _parse_targets(self) -> Iterator[str]:
        """
        Parse targets defined by specific input options

        :return: An iterator of strings
        """
        if self.args.stdin is True:
            yield from self._read_from_stdin()
        elif self.args.from_file is not None:
            yield from self._read_from_file()
        else:
            yield from self._read_from_cli_option(self.args.targets)

    def _set_targets(self) -> tuple[str]:
        """
        Set the "target" attribute of the CLI parser

        :return: A tuple of strings containing domain names to target
        """
        if len(targets := tuple(self._parse_targets())) == 0:
            raise TargetSpecificationError(
                "No targets were specified. Cannot proceed with subdomain "
                "enumeration. Review input settings and try again."
            )
        return targets
