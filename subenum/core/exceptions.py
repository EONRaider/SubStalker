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


class EnumeratorException(Exception):
    def __init__(self, message: str, code: int):
        super().__init__(f"{self.__class__.__name__}: {message}")
        self.code = code


class TargetSpecificationError(EnumeratorException):
    def __init__(self, message: str, code: int = 1):
        super().__init__(message, code)


class FileReadError(EnumeratorException):
    def __init__(self, message: str, code: int = 1):
        super().__init__(message, code)
