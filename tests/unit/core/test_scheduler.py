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
import pytest

from subenum.core.scheduler import Scheduler


def task():
    print("Task completed", end="")


class TestScheduler:
    def test_execute_job_once(self, capsys):
        Scheduler(task=task).execute()
        assert capsys.readouterr().out  # <- Add breakpoint to inspect

    def test_execute_repeated_job(self, capsys):
        Scheduler(task=task, interval=1).execute(2)
        assert capsys.readouterr().out  # <- Add breakpoint to inspect

    def test_init_invalid_interval(self):
        with pytest.raises(TypeError):
            Scheduler(task=task, interval="invalid").execute()
