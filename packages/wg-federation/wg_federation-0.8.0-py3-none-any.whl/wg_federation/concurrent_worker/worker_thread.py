from threading import Event, Timer
from typing import Callable


class WorkerThread(Timer):
    """
    Extension of Timer(Thread).
    Adds another event called `waiting` so that thread pools can know when a Timer is waiting
    """
    interval: int = None
    function: Callable = None
    args = None
    kwargs = None
    finished: Event = None
    waiting: Event = None
    blocking_event: Event = None
    blocking_event_timeout: int = None

    # pylint: disable=too-many-arguments
    def __init__(
            self,
            interval: int,
            function,
            blocking_event: Event = None,
            blocking_event_timeout: int = 60,
            args=None,
            kwargs=None
    ) -> None:
        """
        Constructor
        :param interval:
        :param function:
        :param blocking_event:
        :param blocking_event_timeout:
        :param args:
        :param kwargs:
        """
        super().__init__(interval, function, args, kwargs)
        self.blocking_event = blocking_event
        self.blocking_event_timeout = blocking_event_timeout
        self.waiting = Event()

    def run(self) -> None:
        """ Run the Thread """
        self.waiting.set()
        self.finished.wait(self.interval)
        if self.blocking_event:
            self.blocking_event.wait(self.blocking_event_timeout)
        self.waiting.clear()
        if not self.finished.is_set():
            self.function(*self.args, **self.kwargs)
        self.finished.set()
