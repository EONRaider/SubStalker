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
from subenum.core.processors.file import FileOutput
from subenum.core.types import EnumerationPublisher


class TestFile:
    def test_file_init(self, tmp_path, mock_enumerator):
        mock_enumerator.output_file = tmp_path / "test_file.txt"
        file_output = FileOutput(subject=mock_enumerator)
        assert isinstance(file_output.subject, EnumerationPublisher)

    def test_file_startup(self, tmp_path, mock_enumerator):
        mock_enumerator.output_file = tmp_path / "test_file.txt"
        file_output = FileOutput(mock_enumerator)
        file_output.startup()
        file_output.file.close()

    def test_file_update(
        self, tmp_path, mock_enumerator, api_response_1, api_response_2, api_response_3
    ):
        test_file = tmp_path / "test_file.txt"
        mock_enumerator.output_file = test_file
        file_output = FileOutput(mock_enumerator)

        file_output.file = test_file.open(mode="a", encoding="utf_8")
        for response in api_response_1, api_response_2, api_response_3:
            file_output.update(response)
        file_output.file.close()

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
        test_file = tmp_path / "test_file.txt"
        mock_enumerator.output_file = test_file
        file_output = FileOutput(mock_enumerator)
        file_output.file = test_file.open(mode="a", encoding="utf_8")
        file_output.cleanup()

        captured = capsys.readouterr()

        assert captured.out == (
            f"[+] Enumeration results successfully written to {file_output.file.name}\n"
        )

    def test_inaccessible_file_path(self, mock_enumerator):
        mock_enumerator.output_file = (path := "/root/some/file")
        with pytest.raises(FileReadError) as e:
            FileOutput(mock_enumerator).startup()
        assert (
            e.value.args[0]
            == f"FileReadError: PermissionError: Error accessing specified file path "
            f'"{path}"'
        )
