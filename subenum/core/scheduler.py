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

import itertools
import time

import schedule


class Scheduler:
    def __init__(self, task, interval: int = 0):
        self.task = task
        self.interval = interval

    @property
    def interval(self):
        return self._interval

    @interval.setter
    def interval(self, value: int):
        if not isinstance(value, int):
            raise TypeError(
                f"Cannot set the scheduler's time interval to non-integer value {value}"
            )
        self._interval = value
        schedule.every(value).seconds.do(self.task)

    @staticmethod
    def execute(repeat: int = 0):
        schedule.run_all()
        for i in itertools.count(1):
            if i == repeat:
                break
            schedule.run_pending()
            time.sleep(1)
