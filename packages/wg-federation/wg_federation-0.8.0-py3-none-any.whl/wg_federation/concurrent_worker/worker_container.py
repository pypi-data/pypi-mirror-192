import datetime
import logging

from wg_federation.concurrent_worker.worker import Worker
from wg_federation.concurrent_worker.worker_thread import WorkerThread


class WorkerContainer:
    """
    Container for Worker. Accept Worker registration and run them in concurrent threads
    See this package documentation for more information.
    """
    _threads: dict[str, WorkerThread] = None

    _logger: logging.Logger = None

    def __init__(self, logger: logging.Logger):
        self._threads = {}
        self._logger = logger

    def register(self, worker: Worker):
        """
        Register a new Worker.
        If already registered but not running or waiting, the new Worker will override the previously registered Worker.
        If already registered and running, the registration will fail with a warning raised.
        :param worker:
        :return:
        """
        if worker.get_name() in self._threads:
            if not self._threads[worker.get_name()].waiting.is_set() and self._threads[worker.get_name()].is_alive():
                self._logger.warning(f'Did not register the Worker “{worker.get_name()}” as it is currently running.')
                return

            if self._threads[worker.get_name()].waiting.is_set():
                self._logger.debug(
                    f'Canceling the previously registered Worker “{worker.get_name()}” as it is not yet running.'
                )
                self._threads[worker.get_name()].cancel()
                del self._threads[worker.get_name()]

        worker.pre_register()

        timer = WorkerThread(
            interval=self.__determine_wait_interval(worker), function=worker.run, blocking_event=worker.wait_for()
        )
        timer.name = worker.get_name()
        self._threads[worker.get_name()] = timer

    def start_all(self):
        """
        Starts all the registered Workers concurrently.
        Workers with the `must_wait` attributes will be set to wait `must_wait` seconds before running.
        Also un-registers Workers that finished running through a previous call of this method.
        :return:
        """
        for name, timer in self._threads.copy().items():
            if timer.waiting.is_set() or timer.is_alive():
                self._logger.debug(f'{timer.name} was queued to run again, but it is already waiting before running.')
                continue

            if timer.finished.is_set():
                self._logger.debug(f'{timer.name} has been run. De-registering it.')
                del self._threads[name]
                continue

            timer.start()

    def join_all(self):
        """
        Block the program until all the registered Worker finishes.
        Also un-registers all of them.
        :return:
        """
        for name, timer in self._threads.copy().items():
            timer.join()
            del self._threads[name]

    def __determine_wait_interval(self, worker: Worker) -> int:
        if not worker.wait_date():
            return worker.wait_seconds()

        return max(0, round((worker.wait_date() - datetime.datetime.now()).total_seconds()))
