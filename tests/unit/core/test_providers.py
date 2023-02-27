"""
SubStalker: Find subdomains belonging to given target hosts
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
    <https://github.com/EONRaider/SubStalker/blob/master/LICENSE>.
"""

import pytest
from reconlib.core.exceptions import APIKeyError
from reconlib.crtsh.api import CRTShAPI
from reconlib.hackertarget.api import HackerTargetAPI
from reconlib.virustotal.api import VirusTotalAPI

from substalker.core.providers import (
    crtsh,
    hackertarget,
    virustotal,
    open_providers,
    auth_providers,
)


class TestAPIs:
    def test_crtsh(self):
        """
        GIVEN a function that returns an instance of CRTShAPI
        WHEN this function is called
        THEN this function must return the instance without exceptions
            as well as be registered as an element of the
            "open_providers" list
        """
        assert isinstance(crtsh(), CRTShAPI)
        assert crtsh in open_providers

    def test_hackertarget(self):
        """
        GIVEN a function that returns an instance of HackerTargetAPI
        WHEN this function is called
        THEN this function must return the instance without exceptions
            as well as be registered as an element of the
            "open_providers" list
        """
        assert isinstance(hackertarget(), HackerTargetAPI)
        assert hackertarget in open_providers

    def test_virustotal_env_key(self, api_key, setup_virustotal_api_key):
        """
        GIVEN a function that returns an instance of VirusTotalAPI
        WHEN this function is called and the API keys is set as an
            environment variable
        THEN this function must return the instance without exceptions
            as well as be registered as an element of the
            "auth_providers" list
        """
        assert isinstance((provider := virustotal()), VirusTotalAPI)
        assert provider.api_key == api_key
        assert virustotal in auth_providers

    def test_virustotal_init_key(self, api_key):
        """
        GIVEN a function that returns an instance of VirusTotalAPI
        WHEN this function is called and the API keys is set as an
            argument to the initializer
        THEN this function must return the instance without exceptions
            as well as be registered as an element of the
            "auth_providers" list
        """
        assert isinstance(
            (provider := virustotal(virustotal_auth=api_key)), VirusTotalAPI
        )
        assert provider.api_key == api_key
        assert virustotal in auth_providers

    def test_virustotal_invalid_key(self):
        """
        GIVEN a function that returns an instance of VirusTotalAPI
        WHEN this function is called and no API keys are provided
        THEN an APIKeyError exception must be raised
        """
        with pytest.raises(APIKeyError):
            virustotal()
