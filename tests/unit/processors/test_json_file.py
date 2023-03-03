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

import json
import logging

import pytest

from substalker.core.exceptions import FileReadError
from substalker.core.processors.json_file import JSONFileOutput
from substalker.core.types.base import EnumerationPublisher


class TestJSONFile:
    def test_file_init(self, tmp_path, passive_enumerator):
        """
        GIVEN a valid path to a file
        WHEN this path is passed as an initialization argument to an
            instance of JSONFileOutput
        THEN the JSONFileOutput observer must accept that instance
            without exceptions
        """
        json_output = JSONFileOutput(
            subject=passive_enumerator, path=tmp_path.joinpath("test_file.txt")
        )
        assert isinstance(json_output.subject, EnumerationPublisher)

    def test_json_update(
        self,
        tmp_path,
        passive_enumerator,
        api_response_1,
        api_response_2,
        api_response_3,
    ):
        """
        GIVEN a valid path to a file
        WHEN this path is passed as an initialization argument to an
            instance of JSONFileOutput
        THEN the JSONFileOutput observer must be able to write a
            JSON-formatted string with results to the file without
            exceptions
        """
        json_output = JSONFileOutput(
            subject=passive_enumerator, path=tmp_path.joinpath("test_file.txt")
        )

        for response in api_response_1, api_response_2, api_response_3:
            json_output.update(response)

        assert dict(json_output.results) == {
            "other-target-domain.com.br": {
                "InstanceOfExternalService2": [
                    "sub1.other-target-domain.com.br",
                    "sub2.other-target-domain.com.br",
                    "sub3.other-target-domain.com.br",
                    "sub4.other-target-domain.com.br",
                    "sub5.other-target-domain.com.br",
                ]
            },
            "nmap.org": {
                "InstanceOfExternalService1": [
                    "sub1.nmap.org",
                    "sub2.nmap.org",
                    "sub3.nmap.org",
                    "sub4.nmap.org",
                    "sub5.nmap.org",
                ],
                "InstanceOfExternalService3": [
                    "sub1.nmap.org",
                    "sub2.nmap.org",
                    "sub3.nmap.org",
                ],
            },
        }

    def test_json_cleanup(
        self,
        tmp_path,
        caplog,
        passive_enumerator,
        api_response_1,
        api_response_2,
        api_response_3,
    ):
        """
        GIVEN a valid path to a file
        WHEN this path is passed as an initialization argument to an
            instance of JSONFileOutput
        THEN the JSONFileOutput observer's "cleanup" method must write
            the contents of the enumeration results without exceptions
        """
        caplog.set_level(logging.INFO)
        json_output = JSONFileOutput(
            subject=passive_enumerator, path=tmp_path.joinpath("test_file.txt")
        )

        for response in api_response_1, api_response_2, api_response_3:
            json_output.update(response)

        json_output.cleanup()

        assert (
            f"Enumeration results successfully written in JSON format to "
            f"{str(json_output.path)}" in caplog.messages
        )

        with open(json_output.path) as file:
            assert json.load(file) == {
                "other-target-domain.com.br": {
                    "InstanceOfExternalService2": [
                        "sub1.other-target-domain.com.br",
                        "sub2.other-target-domain.com.br",
                        "sub3.other-target-domain.com.br",
                        "sub4.other-target-domain.com.br",
                        "sub5.other-target-domain.com.br",
                    ]
                },
                "nmap.org": {
                    "InstanceOfExternalService1": [
                        "sub1.nmap.org",
                        "sub2.nmap.org",
                        "sub3.nmap.org",
                        "sub4.nmap.org",
                        "sub5.nmap.org",
                    ],
                    "InstanceOfExternalService3": [
                        "sub1.nmap.org",
                        "sub2.nmap.org",
                        "sub3.nmap.org",
                    ],
                },
            }

    def test_json_cleanup_invalid_file(self, tmp_path, passive_enumerator):
        """
        GIVEN a path to a file
        WHEN this path is invalid
        THEN a FileReadError exception must be raised
        """
        file_path = "/invalid/path/to/file"
        json_output = JSONFileOutput(subject=passive_enumerator, path=file_path)

        with pytest.raises(FileReadError) as e:
            json_output.cleanup()

        assert (
            e.value.args[0]
            == "FileReadError: FileNotFoundError: Error accessing specified file "
            f'path "{file_path}"'
        )
        assert e.value.code == 1

    def test_json_cleanup_silent_mode(
        self,
        tmp_path,
        caplog,
        passive_enumerator,
        api_response_1,
    ):
        """
        GIVEN a valid path to a file
        WHEN this path is passed as an initialization argument to an
            instance of JSONFileOutput and silent mode is enabled
        THEN the JSONFileOutput observer's "cleanup" method must write
            the contents of the enumeration results without exceptions,
            but supress all output to STDOUT
        """
        caplog.set_level(logging.WARNING)
        json_output = JSONFileOutput(
            subject=passive_enumerator, path=tmp_path.joinpath("test_file.txt")
        )

        json_output.update(api_response_1)

        json_output.cleanup()

        assert len(caplog.messages) == 0
