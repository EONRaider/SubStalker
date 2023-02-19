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


class TestPassiveEnumerator:
    def test_num_found_domains(
        self, passive_enumerator, api_response_1, api_response_2
    ):
        """
        GIVEN a correctly initialized instance of EnumerationPublisher
        WHEN this instance has registered found subdomains
        THEN the "num_found_subdomains" property must return the correct
            value of known subdomains
        """
        passive_enumerator.found_domains[
            api_response_1.domain
        ] = api_response_1.subdomains
        passive_enumerator.found_domains[
            api_response_2.domain
        ] = api_response_2.subdomains
        assert passive_enumerator.num_found_domains == 10
