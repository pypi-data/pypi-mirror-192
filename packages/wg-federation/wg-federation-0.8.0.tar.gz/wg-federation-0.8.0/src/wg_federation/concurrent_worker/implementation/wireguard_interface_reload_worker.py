import logging
import subprocess
from datetime import datetime
from threading import Event
from types import ModuleType

from wg_federation.concurrent_worker.worker import Worker
from wg_federation.data.state.wireguard_configuration import WireguardConfiguration
from wg_federation.state.manager.state_data_manager import StateDataManager


class WireguardInterfaceReloadWorker(Worker[WireguardConfiguration]):
    """ Worker to reload (down/up) system WireGuard interfaces """
    _hashlib: ModuleType = None
    _state_data_manager: StateDataManager = None
    _logger: logging.Logger = None
    _subprocess: ModuleType = None

    # pylint: disable=too-many-arguments
    def __init__(
            self,
            hashlib: ModuleType,
            state_data_manager: StateDataManager,
            logger: logging.Logger,
            subprocess_lib: ModuleType,
            name: str,
            context_data: WireguardConfiguration = None,
            wait_seconds: int = 0,
            wait_date: datetime = None,
            wait_for: Event = None,
            wait_for_timeout: int = 60
    ) -> None:
        """
        Constructor
        :param hashlib:
        :param state_data_manager:
        :param logger:
        :param subprocess_lib:
        :param name:
        :param context_data:
        :param wait_seconds:
        :param wait_date:
        :param wait_for:
        :param wait_for_timeout:
        """
        super().__init__(name, context_data, wait_seconds, wait_date, wait_for, wait_for_timeout)
        self._hashlib = hashlib
        self._state_data_manager = state_data_manager
        self._logger = logger
        self._subprocess = subprocess_lib

    def run(self) -> None:
        self.__stop_interface()
        self.__start_interface()

        self._state_data_manager.update_wireguard_interface_configuration({
            'last_loaded_hash': self._context_data.into_sha256_digest(),
            'last_loaded_date': datetime.now(),
        }, self._context_data)

    def __start_interface(self) -> None:
        self._subprocess.run(
            ['/usr/bin/wg-quick', 'up', str(self._context_data.path)],
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True
        )
        self._logger.debug(f'Interface “{self._context_data.path}” has been brought up.')

    def __stop_interface(self) -> None:
        """
        Stop the running interface.
        Note: any subprocess exception is silenced: the interface might not be already running.
        :return:
        """
        try:
            self._subprocess.run(
                ['/usr/bin/wg-quick', 'down', str(self._context_data.path)],
                stdin=subprocess.PIPE,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True
            )
        except subprocess.CalledProcessError:
            pass
