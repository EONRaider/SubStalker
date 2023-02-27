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

import logging

import pytest

from substalker.core.scheduler import Scheduler


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


class TestScheduler:
    def test_execute_job_once(self, capsys, task):
        """
        GIVEN a callable representing a correctly implemented task
        WHEN this callable is passed as an initialization parameter to
        an instance of Scheduler
        THEN the task must be executed without exceptions
        """
        Scheduler(task).execute()
        assert capsys.readouterr().out  # <- Add breakpoint to inspect

    @pytest.mark.parametrize("invalid_argument", [None, "invalid", [], {}, -1, -1000])
    def test_init_invalid_interval(self, task, invalid_argument):
        """
        GIVEN a callable representing a correctly implemented task
        WHEN this callable is passed as an initialization parameter to
        an instance of Scheduler but an invalid type is passed as an
        interval
        THEN a TypeError exception must be raised
        """
        with pytest.raises(TypeError):
            Scheduler(task, interval=invalid_argument).execute()

    def test_logging_prompts(self, caplog, task):
        """
        GIVEN a callable representing a correctly implemented task
        WHEN this callable is passed as an initialization parameter to
        an instance of Scheduler
        THEN the execution of the task must register all logging prompts
        as expected
        """
        caplog.set_level(logging.DEBUG)
        Scheduler(task).execute()
        assert caplog.messages == [
            "Scheduled task TestTask for execution every 0 seconds",
            "Running *all* 1 jobs with 0s delay in between",
            "Running job Job(interval=0, unit=seconds, do=_run_task, args=(), "
            "kwargs={})",
            "Executing subdomain enumeration task #1",
            'Cancelling job "Job(interval=0, unit=seconds, do=_run_task, args=(), '
            'kwargs={})"',
            "Finished executing 1 subdomain enumeration task",
        ]
