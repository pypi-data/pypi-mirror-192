import configparser
import stat
from collections.abc import Mapping
from enum import Enum
from types import ModuleType

from wg_federation.data.state.hq_state import HQState
from wg_federation.data.state.wireguard_configuration import WireguardConfiguration
from wg_federation.data_transformation.locker.configuration_locker import ConfigurationLocker
from wg_federation.event.hq.hq_event import HQEvent
from wg_federation.event.wg_configuration.wg_configuration_event import WGConfigurationEvent
from wg_federation.observer.event_dispatcher import EventDispatcher
from wg_federation.observer.event_subscriber import EventSubscriber
from wg_federation.utils.utils import Utils


class WireguardInterfaceConfigurationEventSubscriber(EventSubscriber[HQState]):
    """ Creates/Updates WireGuard interfaces """

    _os_lib: ModuleType = None
    _configuration_locker: ConfigurationLocker = None
    _event_dispatcher: EventDispatcher = None

    def __init__(
            self,
            os_lib: ModuleType,
            configuration_locker: ConfigurationLocker,
            event_dispatcher: EventDispatcher,
    ):
        """ Constructor """
        self._os_lib = os_lib
        self._configuration_locker = configuration_locker
        self._event_dispatcher = event_dispatcher

    def get_subscribed_events(self) -> list[Enum]:
        return [
            HQEvent.INTERFACES_CONFIGURATION_BEFORE_CREATE,
            HQEvent.FORUMS_CONFIGURATION_BEFORE_CREATE,
            HQEvent.PHONE_LINES_CONFIGURATION_BEFORE_CREATE,
            HQEvent.INTERFACES_CONFIGURATION_BEFORE_UPDATE,
            HQEvent.FORUMS_CONFIGURATION_BEFORE_UPDATE,
            HQEvent.PHONE_LINES_CONFIGURATION_BEFORE_UPDATE,
        ]

    def run(self, data: WireguardConfiguration) -> WireguardConfiguration:
        if not data.last_loaded_hash:
            self._event_dispatcher.dispatch([WGConfigurationEvent.CONFIGURATION_FILE_BEFORE_CREATE], data)
            Utils.open(str(data.path), 'a++', 'UTF-8')
        else:
            self._event_dispatcher.dispatch([WGConfigurationEvent.CONFIGURATION_FILE_BEFORE_UPDATE], data)

        with self._configuration_locker.lock_exclusively(str(data.path)):
            self.__prepare_ini_file(data)

        if not data.last_loaded_hash:
            self._event_dispatcher.dispatch([WGConfigurationEvent.CONFIGURATION_FILE_CREATED], data)
        else:
            self._event_dispatcher.dispatch([WGConfigurationEvent.CONFIGURATION_FILE_UPDATED], data)

        return data

    def __prepare_ini_file(self, wg_configuration: WireguardConfiguration) -> None:
        self.__empty_wireguard_configuration(wg_configuration)

        config = configparser.ConfigParser(interpolation=None)

        for section, options in wg_configuration.interface.into_wireguard_ini().items():
            if isinstance(options, Mapping):
                config.add_section(section)

                for option_name, option_value in options.items():
                    config[section][option_name] = str(option_value)

                self.__write_wireguard_configuration(wg_configuration, config)

    def should_run(self, data: WireguardConfiguration) -> bool:
        return data.last_loaded_hash != data.into_sha256_digest()

    def __empty_wireguard_configuration(self, wg_configuration: WireguardConfiguration) -> None:
        Utils.open(str(wg_configuration.path), 'w', 'UTF-8')

    def __write_wireguard_configuration(
            self,
            wg_configuration: WireguardConfiguration,
            config: configparser.ConfigParser
    ) -> None:
        with Utils.open(str(wg_configuration.path), 'a++', 'UTF-8') as wg_config:
            config.write(wg_config)

        Utils.chmod(str(wg_configuration.path), stat.S_IREAD | stat.S_IWRITE)
