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

import logging

import pytest

from subenum.core.scheduler import Scheduler


def set_repr(description: str):
    class FuncRepr:
        def __init__(self, func):
            self.func = func
            self.__name__ = func.__name__
            self.__doc__ = func.__doc__

        def __call__(self, *args, **kwargs):
            return self.func(*args, **kwargs)

        def __repr__(self):
            return description

    return FuncRepr


@set_repr(description="TestTask")
def task():
    print("Task completed", end="")


@pytest.mark.timed_test
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

    def test_logging_prompts(self, caplog):
        caplog.set_level(logging.DEBUG)
        Scheduler(task=task, interval=1).execute(2)
        assert caplog.messages == [
            "Scheduled task TestTask for execution every 1 second",
            "Executing task TestTask (run 1/2)",
            "Executing task TestTask (run 2/2)",
            "Running job Job(interval=1, unit=seconds, do=task, args=(), kwargs={})",
            "Execution of 2 tasks was finished successfully",
        ]
