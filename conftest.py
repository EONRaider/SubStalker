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

import os
from pathlib import Path

import pytest

from subenum.core import providers
from subenum.core.types.base import EnumerationResult
from subenum.enumerators.passive import PassiveEnumerator


@pytest.fixture
def root_dir() -> Path:
    return Path(__file__).parent.absolute()


@pytest.fixture
def target_domain_1() -> str:
    return "some-target-domain.com"


@pytest.fixture
def target_domain_2() -> str:
    return "other-target-domain.com.br"


@pytest.fixture
def targets_file(root_dir) -> Path:
    return root_dir.joinpath("tests/unit/parsers/sample_targets.txt")


@pytest.fixture
def config_file(root_dir) -> Path:
    return root_dir.joinpath("tests/unit/parsers/sample_config.ini")


@pytest.fixture
def api_key() -> str:
    return "TOTALLY-LEGIT-API-KEY"


@pytest.fixture
def api_response_1(target_domain_1) -> EnumerationResult:
    return EnumerationResult(
        provider="InstanceOfExternalService1",
        domain=target_domain_1,
        subdomains={f"sub{i}.{target_domain_1}" for i in range(1, 6)},
    )


@pytest.fixture
def api_response_2(target_domain_2) -> EnumerationResult:
    return EnumerationResult(
        provider="InstanceOfExternalService2",
        domain=target_domain_2,
        subdomains={f"sub{i}.{target_domain_2}" for i in range(1, 6)},
    )


@pytest.fixture
def api_response_3(target_domain_1) -> EnumerationResult:
    return EnumerationResult(
        provider="InstanceOfExternalService3",
        domain=target_domain_1,
        subdomains={f"sub{i}.{target_domain_1}" for i in range(1, 4)},
    )


@pytest.fixture()
def setup_virustotal_api_key(api_key):
    os.environ["VIRUSTOTAL_API_KEY"] = api_key
    yield
    os.environ.pop("VIRUSTOTAL_API_KEY", None)


@pytest.fixture
def passive_enumerator(target_domain_1, target_domain_2):
    return PassiveEnumerator(
        targets=(target_domain_1, target_domain_2),
        providers={provider() for provider in providers.open_providers},
        max_threads=10,
        retry_time=60,
        max_retries=3,
    )
