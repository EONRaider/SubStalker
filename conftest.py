import os
from pathlib import Path

import pytest

from subenum.core import providers
from subenum.core.types import EnumResult
from subenum.enumerator import Enumerator


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
def api_response_1(target_domain_1) -> EnumResult:
    return EnumResult(
        provider="InstanceOfExternalService1",
        domain=target_domain_1,
        subdomains={f"sub{i}.{target_domain_1}" for i in range(1, 6)},
    )


@pytest.fixture
def api_response_2(target_domain_2) -> EnumResult:
    return EnumResult(
        provider="InstanceOfExternalService2",
        domain=target_domain_2,
        subdomains={f"sub{i}.{target_domain_2}" for i in range(1, 6)},
    )


@pytest.fixture
def api_response_3(target_domain_1) -> EnumResult:
    return EnumResult(
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
def mock_enumerator(target_domain_1, target_domain_2):
    return Enumerator(
        targets=(target_domain_1, target_domain_2),
        providers={provider() for provider in providers.open_providers},
        max_threads=10,
    )
