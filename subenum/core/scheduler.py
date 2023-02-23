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

import time

import schedule

from subenum.core.types.log import Logger


class Scheduler:
    def __init__(self, task, interval: int = 0):
        """
        Schedule tasks for execution at pre-defined time intervals

        :param task: A callable to be executed by the scheduler
        :param interval: Number of seconds to wait between consecutive
            executions of the callable
        """
        self.logger = Logger(name=self.__class__.__name__)
        self.task = task
        self.interval = interval
        self.tasks_completed: int = 0

    @property
    def interval(self) -> int:
        return self._interval

    @interval.setter
    def interval(self, value: int) -> None:
        """
        Validate and set a time interval (in seconds) for the execution
        of consecutive tasks. Schedules the execution of a job on success.

        :param value: Integer representing the time interval in seconds
        """
        if not isinstance(value, int):
            raise TypeError(
                f"Cannot set the scheduler's time interval to non-integer value {value}"
            )
        self._interval = value
        schedule.every(value).seconds.do(self._run_task, forever=bool(value))
        self.logger.debug(
            f"Scheduled task {self.task} for execution every {value} "
            f"{'second' if value == 1 else 'seconds'}"
        )

    def _run_task(self, forever: bool = False):
        self.logger.info(
            f"Executing subdomain enumeration task #{self.tasks_completed + 1}"
        )
        self.task()
        if not forever:
            """Scheduled tasks will either be executed once or forever.
            They're executed only once if the interval is set to 0
            (default value) and forever (at regular time intervals) if
            set otherwise."""
            return schedule.CancelJob

    def execute(self) -> None:
        """
        Execute all scheduled tasks while the jobs queue is not empty
        """
        schedule.run_all()
        while schedule.get_jobs():
            schedule.run_pending()
            time.sleep(1)
        self.logger.info(
            f"Finished executing {self.tasks_completed} subdomain enumeration "
            f"{'task' if self.tasks_completed == 1 else 'tasks'}"
        )
