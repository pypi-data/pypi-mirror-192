from abc import ABC, abstractmethod
from datetime import datetime
from threading import Event
from typing import Generic, TypeVar, Optional

_ContextDataT = TypeVar('_ContextDataT')


class Worker(ABC, Generic[_ContextDataT]):
    """
    Represent a worker: handles contextual data and expect its child to describe the task to run in `run`
    """

    _context_data: _ContextDataT = None
    _name: str = None
    _wait_seconds: int = None
    _wait_date: datetime = None
    _wait_for: Event = None
    _wait_for_timeout: int = None

    # pylint: disable=too-many-arguments

    def __init__(
            self,
            name: str,
            context_data: _ContextDataT = None,
            wait_seconds: int = 0,
            wait_date: datetime = None,
            wait_for: Event = None,
            wait_for_timeout: int = 60,
    ) -> None:
        """
        Constructor
        :param name: name of the worker
        :param context_data: context data
        :param wait_seconds: delays the run of the worker by this amount of seconds.
        :param wait_date: wait for this specific date before running the worker. Conflict and override wait_seconds.
        :param wait_for: wait for this specific Event before running the worker
        :param wait_for_timeout: timeout for wait_for
        """
        self._name = name
        self._context_data = context_data
        self._wait_seconds = wait_seconds
        self._wait_date = wait_date
        self._wait_for = wait_for
        self._wait_for_timeout = wait_for_timeout

    def pre_register(self) -> None:
        """
        Run before this class is registered in a WorkerContainer
        :return:
        """
        return None

    @abstractmethod
    def run(self) -> None:
        """
        Run the worker, concurrently with Workers also registered in the same WorkerContainer.
        :return:
        """

    def get_name(self) -> str:
        """
        Returns the name of the Worker, that uniquely identifies that Worker for any WorkerContainer.
        :return:
        """
        return self._name

    def wait_seconds(self) -> int:
        """
        Amount of time in seconds this Worker should wait before it is actually run.
        :return:
        """
        return self._wait_seconds

    def wait_date(self) -> Optional[datetime]:
        """
        Wait for this specific date before running the worker.
        :return:
        """
        return self._wait_date

    def wait_for(self) -> Optional[Event]:
        """
        Wait for this specific Event before running the worker
        :return:
        """
        return self._wait_for

    def wait_for_timeout(self) -> int:
        """
        Wait for this specific Event before running the worker
        :return:
        """
        return self._wait_for_timeout
