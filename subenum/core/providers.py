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

from reconlib import CRTShAPI, HackerTargetAPI, VirusTotalAPI


open_providers = []  # APIs that respond to simple, unauthenticated requests
auth_providers = []  # APIs that require keys to respond
all_providers = []


def register_provider(auth_required: bool = False):
    def wrapper(func):
        if auth_required is True:
            auth_providers.append(func)
        else:
            open_providers.append(func)
        all_providers.append(func)
        return func

    return wrapper


@register_provider()
def crtsh():
    return CRTShAPI()


@register_provider()
def hackertarget():
    return HackerTargetAPI()


@register_provider(auth_required=True)
def virustotal(*, virustotal_auth=None, **kwargs):
    return VirusTotalAPI(api_key=virustotal_auth)
