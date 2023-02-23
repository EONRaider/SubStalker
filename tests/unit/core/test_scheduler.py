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


class Task:
    def __init__(self, description: str = "TestTask"):
        self.description = description

    def __call__(self, *args, **kwargs):
        print("Task Completed")

    def __repr__(self):
        return self.description


@pytest.fixture
def task():
    return Task()


@pytest.mark.timed_test
class TestScheduler:
    def test_execute_job_once(self, capsys, task):
        Scheduler(task).execute()
        assert capsys.readouterr().out  # <- Add breakpoint to inspect

    def test_init_invalid_interval(self, task):
        with pytest.raises(TypeError):
            Scheduler(task, interval="invalid").execute()

    def test_logging_prompts(self, caplog, task):
        caplog.set_level(logging.DEBUG)
        Scheduler(task).execute()
        assert caplog.messages == [
            "Scheduled task TestTask for execution every 0 seconds",
            "Running *all* 1 jobs with 0s delay in between",
            "Running job Job(interval=0, unit=seconds, do=_run_task, args=(), "
            "kwargs={'forever': False})",
            "Executing subdomain enumeration task #1",
            'Cancelling job "Job(interval=0, unit=seconds, do=_run_task, args=(), '
            "kwargs={'forever': False})\"",
            "Finished executing 0 subdomain enumeration tasks",
        ]
