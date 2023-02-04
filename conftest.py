import os
from pathlib import Path

import pytest


@pytest.fixture
def root_dir() -> Path:
    return Path(__file__).parent.absolute()


@pytest.fixture
def target_domain() -> str:
    return "some-target-domain.com"


@pytest.fixture
def targets_file(root_dir) -> Path:
    return root_dir.joinpath("tests/unit/cli_parser/sample_targets.txt")


@pytest.fixture
def api_key() -> str:
    return "TOTALLY-LEGIT-API-KEY"


@pytest.fixture()
def setup_virustotal_api_key(api_key):
    os.environ["VIRUSTOTAL_API_KEY"] = api_key
    yield
    os.environ.pop("VIRUSTOTAL_API_KEY", None)
