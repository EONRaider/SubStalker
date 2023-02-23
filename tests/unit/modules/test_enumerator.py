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

from subenum.core.processors.json_file import JSONFileOutput
from subenum.core.processors.screen import ScreenOutput
from subenum.core.processors.text_file import TextFileOutput
from subenum.core.types.base import EnumerationPublisher
from subenum.modules.enumerator import SubdomainEnumerator


class TestSubdomainEnumerator:
    def test_add_enumeration_modules(self, tmp_path, passive_enumerator):
        enumerator = SubdomainEnumerator(
            file_path=tmp_path.joinpath("file.txt"),
            json_path=tmp_path.joinpath("json.txt"),
        )
        enumerator.attach_enumeration_module(passive_enumerator)
        module = enumerator.modules[0]
        assert isinstance(module, EnumerationPublisher)
        assert isinstance(module._observers[0], ScreenOutput)
        assert isinstance(module._observers[1], TextFileOutput)
        assert isinstance(module._observers[2], JSONFileOutput)
