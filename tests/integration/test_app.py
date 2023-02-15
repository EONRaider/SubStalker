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

import logging
import random

from subenum.core.processors.json_file import JSONFileOutput
from subenum.core.processors.text_file import TextFileOutput
from subenum.core.processors.screen import ScreenOutput
from subenum.core.providers import all_providers
from subenum.enumerator import Enumerator


class TestApp:
    def test_run_enumerator(
        self,
        caplog,
        tmp_path,
        mocker,
        target_domain_1,
        api_response_1,
        setup_virustotal_api_key,
    ):
        mocker.patch(
            "subenum.enumerator.Enumerator.query_provider", return_value=api_response_1
        )

        caplog.set_level(logging.INFO)

        text_file = tmp_path.joinpath("text_file.txt")
        json_file = tmp_path.joinpath("json_file.txt")

        enumerator = Enumerator(
            targets=(target_domain_1,),
            providers=[provider() for provider in all_providers],
            max_threads=(num_threads := random.randint(1, 10)),
            retry_time=15,
        )
        screen = ScreenOutput(subject=enumerator)

        TextFileOutput(subject=enumerator, path=text_file)
        JSONFileOutput(subject=enumerator, path=json_file)

        with enumerator:
            for _ in enumerator.execute():
                pass

        assert caplog.messages == [
            f"Subdomain enumerator started with {num_threads} "
            f"thread{'s' if num_threads > 1 else ''} for {target_domain_1}",
            "\t[InstanceOfExternalService1] sub1.some-target-domain.com",
            "\t[InstanceOfExternalService1] sub2.some-target-domain.com",
            "\t[InstanceOfExternalService1] sub3.some-target-domain.com",
            "\t[InstanceOfExternalService1] sub4.some-target-domain.com",
            "\t[InstanceOfExternalService1] sub5.some-target-domain.com",
            f"Enumeration of 1 domain was completed in "
            f"{enumerator.total_time:.2f} seconds and found "
            f"{screen.subject.num_found_domains} subdomains",
            f"Enumeration results successfully written in text format to {text_file}",
            f"Enumeration results successfully written in JSON format to {json_file}",
        ]
