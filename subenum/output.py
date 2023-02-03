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

from abc import ABC, abstractmethod


class EnumerationSubscriber(ABC):
    def __init__(self, subject):
        subject.register(self)
        self.subject = subject

    @abstractmethod
    def update(self, domains) -> None:
        ...

    @abstractmethod
    def end_output(self) -> None:
        ...


class ScreenOutput(EnumerationSubscriber):
    def __init__(self, subject):
        super().__init__(subject)

    def update(self, domains) -> None:
        for domain in domains:
            print(f"{domain}")

    def end_output(self) -> None:
        pass


class FileOutput(EnumerationSubscriber):
    def __init__(self, subject):
        super().__init__(subject)
        self.output_filepath = subject.output_file
        self.output_file = open(subject.output_file, mode="w", encoding="utf-8")

    def update(self, domains) -> None:
        for domain in domains:
            self.output_file.write(f"{domain}\n")

    def end_output(self) -> None:
        self.output_file.close()
