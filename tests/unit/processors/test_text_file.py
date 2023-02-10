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
import pytest

from subenum.core.exceptions import FileReadError
from subenum.core.processors.text_file import TextFileOutput
from subenum.core.types import EnumerationPublisher


class TestFile:
    def test_file_init(self, tmp_path, mock_enumerator):
        """
        GIVEN a valid path to a file
        WHEN this path is passed as the output file of an instance of
            EnumerationPublisher
        THEN the FileOutput observer must accept that instance without
            exceptions
        """
        file_output = TextFileOutput(
            subject=mock_enumerator, path=tmp_path.joinpath("test_file.txt")
        )
        assert isinstance(file_output.subject, EnumerationPublisher)

    def test_file_startup(self, tmp_path, mock_enumerator):
        """
        GIVEN a valid path to a file
        WHEN this path is passed as the output file of an instance of
            EnumerationPublisher
        THEN the FileOutput observer must be able to open and close the
            file descriptor without exceptions
        """
        file_output = TextFileOutput(
            subject=mock_enumerator, path=tmp_path.joinpath("test_file.txt")
        )
        file_output.startup()
        file_output.fd.close()

    def test_file_update(
        self, tmp_path, mock_enumerator, api_response_1, api_response_2, api_response_3
    ):
        """
        GIVEN a valid path to a file
        WHEN this path is passed as the output file of an instance of
            EnumerationPublisher
        THEN the FileOutput observer must be able to write de-duplicated
            results to the file without exceptions
        """
        test_file = tmp_path / "test_file.txt"
        file_output = TextFileOutput(subject=mock_enumerator, path=test_file)

        file_output.fd = test_file.open(mode="a", encoding="utf_8")
        for response in api_response_1, api_response_2, api_response_3:
            file_output.update(response)
            mock_enumerator.found_domains[response.domain] |= response.subdomains
        file_output.fd.close()

        with open(test_file) as file:
            written_results = file.readlines()

        assert written_results == [
            "sub1.some-target-domain.com\n",
            "sub2.some-target-domain.com\n",
            "sub3.some-target-domain.com\n",
            "sub4.some-target-domain.com\n",
            "sub5.some-target-domain.com\n",
            "sub1.other-target-domain.com.br\n",
            "sub2.other-target-domain.com.br\n",
            "sub3.other-target-domain.com.br\n",
            "sub4.other-target-domain.com.br\n",
            "sub5.other-target-domain.com.br\n",
        ]

    def test_file_cleanup(self, capsys, tmp_path, mock_enumerator):
        """
        GIVEN a valid path to a file
        WHEN this path is passed as the output file of an instance of
            EnumerationPublisher
        THEN the FileOutput observer's "cleanup" method must return its
            output without exceptions
        """
        test_file = tmp_path / "test_file.txt"
        file_output = TextFileOutput(subject=mock_enumerator, path=test_file)
        file_output.fd = test_file.open(mode="a", encoding="utf_8")
        file_output.cleanup()

        captured = capsys.readouterr()

        assert captured.out == (
            f"[+] Enumeration results successfully written to {file_output.fd.name}\n"
        )

    def test_inaccessible_file_path(self, mock_enumerator):
        """
        GIVEN a valid but inaccessible path to a file
        WHEN this path is passed as the output file of an instance of
            EnumerationPublisher
        THEN a FileReadError exception must be raised
        """
        test_file = "/root/some/file"
        with pytest.raises(FileReadError) as e:
            TextFileOutput(subject=mock_enumerator, path=test_file).startup()
        assert (
            e.value.args[0]
            == f"FileReadError: PermissionError: Error accessing specified file path "
            f'"{test_file}"'
        )
