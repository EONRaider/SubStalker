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
from substalker.core.exceptions import EnumeratorException


class TestExceptions:
    @pytest.mark.parametrize("exception", EnumeratorException.__subclasses__())
    def test_enumerator_exception(self, exception):
        """
        GIVEN the EnumeratorException base class
        WHEN one of its subclasses is raised
        THEN a given exception message and code must be present when the
            exception is raised
        """
        message = "Something went wrong"
        with pytest.raises(exception) as e:
            raise exception(message, code=1337)
        assert e.value.args[0] == f"{exception.__name__}: {message}"
        assert e.value.code == 1337
