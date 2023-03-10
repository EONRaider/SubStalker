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

import io
import itertools
import sys
from argparse import Namespace

import pytest

from subenum.cli_parser import CLIArgumentsParser


class TestCLIArgumentsParser:
    def test_parse_single_target_from_stdin(self, target_domain):
        """
        GIVEN a string representing a domain name
        WHEN this string is read from the STDIN
        THEN a correctly instantiated Namespace object containing the
            domain name as an attribute must be returned from the CLI
            arguments parser
        """
        sys.stdin = io.StringIO(target_domain)
        parser = CLIArgumentsParser()

        assert parser.parse(["--stdin"]) == Namespace(
            targets=(target_domain,),
            from_file=None,
            stdin=True,
            output=None,
            max_threads=CLIArgumentsParser.max_threads,
        )

    def test_parse_multiple_targets_from_stdin(self, target_domain):
        """
        GIVEN a string representing line-separated domain names
        WHEN this string is read from the STDIN
        THEN a correctly instantiated Namespace object containing a
            tuple composed of each domain name must be returned from the
            CLI arguments parser as an attribute
        """
        domains_str = "\n".join(d for d in itertools.repeat(target_domain, 3))
        sys.stdin = io.StringIO(domains_str)
        parser = CLIArgumentsParser()

        assert parser.parse(["--stdin"]) == Namespace(
            targets=tuple(domains_str.split("\n")),
            from_file=None,
            stdin=True,
            output=None,
            max_threads=CLIArgumentsParser.max_threads,
        )

    def test_parse_single_target_from_cli(self, target_domain):
        """
        GIVEN a string representing a domain name
        WHEN this string is passed as an argument to the appropriate CLI
            option
        THEN a correctly instantiated Namespace object containing the
            domain name as an attribute must be returned from the CLI
            arguments parser
        """
        parser = CLIArgumentsParser()

        assert parser.parse(["--targets", target_domain]) == Namespace(
            targets=(target_domain,),
            from_file=None,
            stdin=False,
            output=None,
            max_threads=CLIArgumentsParser.max_threads,
        )

    def test_parse_multiple_targets_from_cli(self, target_domain):
        """
        GIVEN a string representing a sequence of comma-separated domain
            names
        WHEN this string is passed as an argument to the appropriate CLI
            option
        THEN a correctly instantiated Namespace object containing a
            tuple composed of each domain name must be returned from the
            CLI arguments parser as an attribute
        """
        parser = CLIArgumentsParser()
        domains_str = ", ".join(d for d in itertools.repeat(target_domain, 3))

        assert parser.parse(["--targets", domains_str]) == Namespace(
            targets=tuple(domains_str.split(", ")),
            from_file=None,
            stdin=False,
            output=None,
            max_threads=CLIArgumentsParser.max_threads,
        )

    def test_parse_targets_from_file(self, targets_file):
        """
        GIVEN a string representing a path to a file
        WHEN this string is passed as an argument to the appropriate CLI
            option and its contents consist of line-separated domain
            names
        THEN a correctly instantiated Namespace object containing a
            tuple composed of each domain name must be returned from the
            CLI arguments parser as an attribute
        """
        parser = CLIArgumentsParser()

        with open(targets_file, encoding="utf_8") as file:
            file_targets = tuple(target.strip() for target in file.readlines())

        assert parser.parse(["--from-file", str(targets_file)]) == Namespace(
            targets=file_targets,
            from_file=str(targets_file),
            stdin=False,
            output=None,
            max_threads=CLIArgumentsParser.max_threads,
        )

    def test_parse_targets_from_non_existent_file(self):
        """
        GIVEN a string representing a path to a non-existent file
        WHEN this string is passed as an argument to the appropriate CLI
            option
        THEN a FileNotFoundError exception must be raised
        """
        parser = CLIArgumentsParser()
        invalid_path = "/invalid/path/to/file"

        with pytest.raises(SystemExit) as e:
            parser.parse(["--from-file", invalid_path])

        assert (
            e.value.args[0]
            == f"[!] FileNotFoundError: Failed to read file {invalid_path}"
        )

    def test_parse_targets_from_inaccessible_file(self):
        """
        GIVEN a string representing a path to a file to which the
            current user has no read/write privileges
        WHEN this string is passed as an argument to the appropriate CLI
            option
        THEN a PermissionError exception must be raised
        """
        parser = CLIArgumentsParser()

        """Provoke a PermissionError when tests are run without root
        privileges"""
        invalid_path = "/root/some/file"

        with pytest.raises(SystemExit) as e:
            parser.parse(["--from-file", invalid_path])

        assert (
            e.value.args[0]
            == f"[!] PermissionError: Failed to read file {invalid_path}"
        )
