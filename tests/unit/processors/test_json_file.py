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
import json

import pytest

from subenum.core.exceptions import FileReadError
from subenum.core.processors.json_file import JSONFileOutput
from subenum.core.types import EnumerationPublisher


class TestJSONFile:
    def test_file_init(self, tmp_path, mock_enumerator):
        """
        GIVEN a valid path to a file
        WHEN this path is passed as an initialization argument to an
            instance of JSONFileOutput
        THEN the JSONFileOutput observer must accept that instance
            without exceptions
        """
        json_output = JSONFileOutput(
            subject=mock_enumerator, path=tmp_path.joinpath("test_file.txt")
        )
        assert isinstance(json_output.subject, EnumerationPublisher)

    def test_json_update(
        self, tmp_path, mock_enumerator, api_response_1, api_response_2, api_response_3
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
            subject=mock_enumerator, path=tmp_path.joinpath("test_file.txt")
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
            "some-target-domain.com": {
                "InstanceOfExternalService1": [
                    "sub1.some-target-domain.com",
                    "sub2.some-target-domain.com",
                    "sub3.some-target-domain.com",
                    "sub4.some-target-domain.com",
                    "sub5.some-target-domain.com",
                ],
                "InstanceOfExternalService3": [
                    "sub1.some-target-domain.com",
                    "sub2.some-target-domain.com",
                    "sub3.some-target-domain.com",
                ],
            },
        }

    def test_json_cleanup(
        self, tmp_path, mock_enumerator, api_response_1, api_response_2, api_response_3
    ):
        """
        GIVEN a valid path to a file
        WHEN this path is passed as an initialization argument to an
            instance of JSONFileOutput
        THEN the JSONFileOutput observer's "cleanup" method must write
            the contents of the enumeration results without exceptions
        """
        json_output = JSONFileOutput(
            subject=mock_enumerator, path=tmp_path.joinpath("test_file.txt")
        )

        for response in api_response_1, api_response_2, api_response_3:
            json_output.update(response)

        json_output.cleanup()

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
                "some-target-domain.com": {
                    "InstanceOfExternalService1": [
                        "sub1.some-target-domain.com",
                        "sub2.some-target-domain.com",
                        "sub3.some-target-domain.com",
                        "sub4.some-target-domain.com",
                        "sub5.some-target-domain.com",
                    ],
                    "InstanceOfExternalService3": [
                        "sub1.some-target-domain.com",
                        "sub2.some-target-domain.com",
                        "sub3.some-target-domain.com",
                    ],
                },
            }

    def test_json_cleanup_invalid_file(self, tmp_path, mock_enumerator):
        """
        GIVEN a path to a file
        WHEN this path is invalid
        THEN a FileReadError exception must be raised
        """
        file_path = "/invalid/path/to/file"
        json_output = JSONFileOutput(subject=mock_enumerator, path=file_path)

        with pytest.raises(FileReadError) as e:
            json_output.cleanup()

        assert (
            e.value.args[0]
            == "FileReadError: FileNotFoundError: Error accessing specified file "
            f'path "{file_path}"'
        )
        assert e.value.code == 1
