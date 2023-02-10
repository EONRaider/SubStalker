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
        """
        GIVEN a correctly initialized instance of EnumerationPublisher
        WHEN this instance is passed as the subject to a ScreenOutput
            observer
        THEN the instance of ScreenOutput must be initialized without
            exceptions
        """
        screen = ScreenOutput(subject=mock_enumerator)
        assert isinstance(screen.subject, Enumerator)

    def test_screen_startup(self, capsys, mock_enumerator):
        """
        GIVEN a correctly initialized instance of EnumerationPublisher
        WHEN this instance is passed as the subject to a ScreenOutput
            observer
        THEN the "startup" method of ScreenOutput must be able to access
            the subject's attributes and display its output without
            exceptions
        """
        screen = ScreenOutput(subject=mock_enumerator)
        screen.startup(mock_enumerator)
        assert capsys.readouterr().out == (
            f"[+] Subdomain enumerator started with {mock_enumerator.max_threads} "
            f"threads for {' | '.join(mock_enumerator.targets)}\n\n"
        )

    def test_screen_update(
        self, capsys, mock_enumerator, api_response_1, api_response_2, api_response_3
    ):
        """
        GIVEN a correctly initialized instance of EnumerationPublisher
        WHEN this instance is passed as the subject to a ScreenOutput
            observer
        THEN the "update" method of ScreenOutput must be able to register
            and display any domains passed as a result regardless of
            their origin
        """
        screen = ScreenOutput(subject=mock_enumerator)
        for response in api_response_1, api_response_2, api_response_3:
            screen.update(response)
            mock_enumerator.found_domains[response.domain] |= response.subdomains

        assert capsys.readouterr().out == (
            "[InstanceOfExternalService1] sub1.some-target-domain.com\n"
            "[InstanceOfExternalService1] sub2.some-target-domain.com\n"
            "[InstanceOfExternalService1] sub3.some-target-domain.com\n"
            "[InstanceOfExternalService1] sub4.some-target-domain.com\n"
            "[InstanceOfExternalService1] sub5.some-target-domain.com\n"
            "[InstanceOfExternalService2] sub1.other-target-domain.com.br\n"
            "[InstanceOfExternalService2] sub2.other-target-domain.com.br\n"
            "[InstanceOfExternalService2] sub3.other-target-domain.com.br\n"
            "[InstanceOfExternalService2] sub4.other-target-domain.com.br\n"
            "[InstanceOfExternalService2] sub5.other-target-domain.com.br\n"
        )

    def test_screen_cleanup(self, capsys, mock_enumerator):
        """
        GIVEN a correctly initialized instance of EnumerationPublisher
        WHEN this instance is passed as the subject to a ScreenOutput
            observer
        THEN the "cleanup" method of ScreenOutput must be able to access
            the subject's attributes and display its output without
            exceptions
        """
        mock_enumerator.total_time = 1
        (screen := ScreenOutput(subject=mock_enumerator)).cleanup()
        assert (
            capsys.readouterr().out
            == f"\n[+] Enumeration of {len(mock_enumerator.targets)} domains was "
            f"completed in {mock_enumerator.total_time:.2f} seconds and found "
            f"{screen.subject.num_found_domains} subdomains\n"
        )

    def test_silent_mode(self, capsys, mock_enumerator, api_response_1):
        """
        GIVEN a correctly initialized instance of EnumerationPublisher
        WHEN this instance is passed as the subject to a ScreenOutput
            observer
        THEN the methods of ScreenOutput responsible for displaying
            output must be able to correctly format their messages
        """
        screen = ScreenOutput(subject=mock_enumerator, silent_mode=True)
        screen.startup(mock_enumerator)
        screen.update(api_response_1)
        screen.cleanup()

        assert capsys.readouterr().out == (
            "sub1.some-target-domain.com\n"
            "sub2.some-target-domain.com\n"
            "sub3.some-target-domain.com\n"
            "sub4.some-target-domain.com\n"
            "sub5.some-target-domain.com\n"
        )
