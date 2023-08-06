import datetime
from enum import Enum
from types import ModuleType
from typing import Optional

from dependency_injector.providers import Factory

from wg_federation.concurrent_worker.worker_container import WorkerContainer
from wg_federation.data.input.user_input import UserInput
from wg_federation.data.state.wireguard_configuration import WireguardConfiguration
from wg_federation.event.wg_configuration.wg_configuration_event import WGConfigurationEvent
from wg_federation.observer.event_subscriber import EventSubscriber


class WireguardInterfaceSystemReloadEventSubscriber(EventSubscriber[WireguardConfiguration]):
    """ Reload (down and up) underlying system WireGuard interfaces """

    _user_input: UserInput = None
    _delayed_tasks: WorkerContainer = None
    _wireguard_interface_reload_worker_factory: Factory = None
    _hashlib: ModuleType = None

    def __init__(
            self,
            user_input: UserInput,
            delayed_tasks: WorkerContainer,
            wireguard_interface_reload_worker_factory: Factory,
            hashlib: ModuleType,
    ) -> None:
        """
        Constructor
        :param user_input:
        :param delayed_tasks:
        :param wireguard_interface_reload_worker_factory:
        :param hashlib:
        """
        self._user_input = user_input
        self._delayed_tasks = delayed_tasks
        self._wireguard_interface_reload_worker_factory: Factory = wireguard_interface_reload_worker_factory
        self._hashlib = hashlib

    def get_subscribed_events(self) -> list[Enum]:
        return [
            WGConfigurationEvent.CONFIGURATION_FILE_CREATED,
            WGConfigurationEvent.CONFIGURATION_FILE_UPDATED,
        ]

    def run(self, data: WireguardConfiguration) -> WireguardConfiguration:
        self._delayed_tasks.register(self._wireguard_interface_reload_worker_factory(
            name='wireguard_interface_reload_' + data.name,
            context_data=data,
            wait_date=self.__do_not_reload_before_date(data.last_loaded_date)
        ))

        return data

    def should_run(self, data: WireguardConfiguration) -> bool:
        return data.path.exists() and \
            data.last_loaded_hash != data.into_sha256_digest() and \
            self.__user_input_requires_restart()

    def __user_input_requires_restart(self):
        return self._user_input.arg1 == 'run' or self._user_input.wg_interface_restart

    def __do_not_reload_before_date(self, last_loaded_date: datetime.datetime) -> Optional[datetime.datetime]:
        """
        :param last_loaded_date:
        :return:
        """
        if not last_loaded_date:
            return None

        return last_loaded_date + datetime.timedelta(0, 5)
