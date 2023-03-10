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
import re
import sys
from collections.abc import Iterator


class CLIArgumentsParser:
    max_threads = 10

    def __init__(self):
        self.parser = argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description="Find subdomains belonging to given target hosts using active"
            "and passive enumeration methods",
        )
        self.targeting = self.parser.add_mutually_exclusive_group(required=True)
        self.args = None

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
        self.parser.add_argument(
            "-o",
            "--output",
            type=str,
            help="Absolute path to a file to which enumeration results will be written",
        )
        self.parser.add_argument(
            "--max-threads",
            type=int,
            help=f"Maximum number of threads to use when enumerating subdomains "
            f"(defaults to {self.max_threads})",
            default=self.max_threads,
        )
        self.args = self.parser.parse_args(*args, **kwargs)
        self.args.targets = tuple(self.parse_targets())
        return self.args

    @staticmethod
    def _read_from_stdin() -> Iterator[str]:
        yield from (line.strip() for line in sys.stdin.readlines())

    def _read_from_file(self) -> Iterator[str]:
        try:
            with open(self.args.from_file, encoding="utf_8") as file:
                yield from (line.strip() for line in file.readlines())
        except OSError as e:
            raise SystemExit(
                f"[!] {e.__class__.__name__}: Failed to read file "
                f"{str(self.args.from_file)}"
            )

    def _read_from_cli_option(self) -> Iterator[str]:
        yield from re.split(r"\s*,\s*", self.args.targets)

    def parse_targets(self) -> Iterator[str]:
        if self.args.stdin is True:
            yield from self._read_from_stdin()
        elif self.args.from_file is not None:
            yield from self._read_from_file()
        else:
            yield from self._read_from_cli_option()
