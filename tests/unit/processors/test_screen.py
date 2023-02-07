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

from subenum.core.processors.screen import ScreenOutput
from subenum.enumerator import Enumerator


class TestScreen:
    def test_screen_init(self, mock_enumerator):
        screen = ScreenOutput(subject=mock_enumerator)
        assert isinstance(screen.subject, Enumerator)

    def test_screen_startup(self, capsys, api_response, mock_enumerator):
        screen = ScreenOutput(subject=mock_enumerator)
        screen.startup(mock_enumerator)
        captured = capsys.readouterr()
        assert captured.out == (
            "[+] Subdomain enumerator started with 10 threads for "
            "some-target-domain.com | some-target-domain.com.br\n"
        )

    def test_screen_update(self, capsys, mock_enumerator, api_response):
        screen = ScreenOutput(subject=mock_enumerator)
        screen.update(api_response)
        captured = capsys.readouterr()
        assert captured.out == (
            "\tsub1.some-target-domain.com\n"
            "\tsub2.some-target-domain.com\n"
            "\tsub3.some-target-domain.com\n"
            "\tsub4.some-target-domain.com\n"
            "\tsub5.some-target-domain.com\n"
        )

    def test_screen_cleanup(self, capsys, mock_enumerator):
        mock_enumerator.total_time = 1
        ScreenOutput(subject=mock_enumerator).cleanup()
        captured = capsys.readouterr()
        assert (
            captured.out
            == f"[+] Enumeration of {len(mock_enumerator.targets)} domains completed "
            f"in {mock_enumerator.total_time:.2f} seconds\n"
        )
