import os
from collections.abc import Mapping
from enum import Enum
from logging import Logger
from typing import Any

from deepmerge import always_merger

from wg_federation.crypto.wireguard_key_generator import WireguardKeyGenerator
from wg_federation.data.input.command_line.secret_retreival_method import SecretRetrievalMethod
from wg_federation.data.input.user_input import UserInput
from wg_federation.data.state.federation import Federation
from wg_federation.data.state.hq_state import HQState
from wg_federation.data.state.interface_kind import InterfaceKind
from wg_federation.data.state.wireguard_configuration import WireguardConfiguration
from wg_federation.data.state.wireguard_interface import WireguardInterface
from wg_federation.data_transformation.configuration_location_finder import ConfigurationLocationFinder
from wg_federation.data_transformation.loader.can_load_configuration_interface import CanLoadConfigurationInterface
from wg_federation.data_transformation.locker.configuration_locker import ConfigurationLocker
from wg_federation.data_transformation.saver.can_save_configuration_interface import CanSaveConfigurationInterface
from wg_federation.event.hq.hq_event import HQEvent
from wg_federation.exception.user.data.state_signature_cannot_be_verified import StateNotBootstrapped
from wg_federation.observer.event_dispatcher import EventDispatcher
from wg_federation.utils.utils import Utils


class StateDataManager:
    """
    Handles wg-federation HQState lifecycles: create, updates and reload form source of truth.
    """
    _configuration_location_finder: ConfigurationLocationFinder = None
    _configuration_loader: CanLoadConfigurationInterface = None
    _configuration_saver: CanSaveConfigurationInterface = None
    _configuration_locker: ConfigurationLocker = None
    _wireguard_key_generator: WireguardKeyGenerator = None
    _event_dispatcher: EventDispatcher = None
    _logger: Logger = None
    _user_input: UserInput = None

    # pylint: disable=too-many-arguments
    def __init__(
            self,
            configuration_location_finder: ConfigurationLocationFinder,
            configuration_loader: CanLoadConfigurationInterface,
            configuration_saver: CanSaveConfigurationInterface,
            configuration_locker: ConfigurationLocker,
            wireguard_key_generator: WireguardKeyGenerator,
            event_dispatcher: EventDispatcher,
            logger: Logger,
            user_input: UserInput,
    ):
        """
        Constructor
        :param configuration_location_finder:
        :param configuration_loader:
        :param configuration_saver:
        :param configuration_locker:
        :param wireguard_key_generator:
        :param event_dispatcher:
        :param logger:
        :param user_input:
        """
        self._configuration_location_finder = configuration_location_finder
        self._configuration_loader = configuration_loader
        self._configuration_saver = configuration_saver
        self._configuration_locker = configuration_locker
        self._wireguard_key_generator = wireguard_key_generator
        self._event_dispatcher = event_dispatcher
        self._logger = logger
        self._user_input = user_input

    def reload(self) -> HQState:
        """
        Loads a HQState from the source of truth.
        :return:
        """
        try:
            with self._configuration_locker.lock_shared(self._configuration_location_finder.state()) as conf_file:
                hq_state = self._reload_from_source(conf_file)

            return hq_state

        except FileNotFoundError as err:
            raise StateNotBootstrapped('Unable to load the state: it was not bootstrapped. Run `hq boostrap`.') from err

    def update_wireguard_interface_configuration(
            self, configuration_changes: dict, current_configuration: WireguardConfiguration
    ) -> WireguardConfiguration:
        """
        Updates a WireguardConfiguration
        :param configuration_changes:
        :param current_configuration:
        :return:
        """
        updated_wg_configuration = WireguardConfiguration.from_dict(
            dict(always_merger.merge(current_configuration.dict(), configuration_changes))
        )

        self._event_dispatcher.dispatch(
            [HQEvent.dynamic_get(updated_wg_configuration.kind, 'CONFIGURATION_BEFORE_UPDATE')],
            updated_wg_configuration
        )

        self.update_hq_state({
            updated_wg_configuration.kind.value: {
                updated_wg_configuration.name: updated_wg_configuration.dict()
            }
        })

        self._event_dispatcher.dispatch(
            [HQEvent.dynamic_get(updated_wg_configuration.kind, 'CONFIGURATION_UPDATED')],
            updated_wg_configuration
        )

        return updated_wg_configuration

    def update_hq_state(self, configuration_changes: dict) -> HQState:
        """
        Updates HQState
        :param configuration_changes:
        :return:
        """
        with self._configuration_locker.lock_exclusively(self._configuration_location_finder.state()) as conf_file:
            hq_state = self._event_dispatcher.dispatch(
                [HQEvent.STATE_BEFORE_UPDATE], self._reload_from_source(conf_file)
            )
            updated_hq_state = HQState.from_dict(
                dict(always_merger.merge(hq_state.dict(exclude_defaults=True), configuration_changes))
            )
            self._configuration_saver.save(updated_hq_state.dict(exclude_defaults=True), conf_file)

        return self._event_dispatcher.dispatch(
            [HQEvent.STATE_UPDATED],
            HQState.from_dict(updated_hq_state.dict(exclude_defaults=True))
        )

    def create_hq_state(self) -> HQState:
        """
        Create a new HQState and save it.
        This method disregard whether a state already exists. To use with precaution.
        :return:
        """

        with self._configuration_locker.lock_exclusively(self._configuration_location_finder.state()) as conf_file:
            state: HQState = self._event_dispatcher.dispatch(
                [HQEvent.STATE_BEFORE_CREATE], self._generate_new_hq_state()
            )

            self._configuration_saver.save(state.dict(), conf_file)

        self._event_dispatcher.dispatch([HQEvent.STATE_CREATED], state)
        self.__dispatch_configuration_events(state.phone_lines, HQEvent.PHONE_LINES_CONFIGURATION_CREATED)
        self.__dispatch_configuration_events(state.forums, HQEvent.FORUMS_CONFIGURATION_CREATED)
        self.__dispatch_configuration_events(state.interfaces, HQEvent.INTERFACES_CONFIGURATION_CREATED)

        return state

    def _reload_from_source(self, source: Any = None) -> HQState:
        self._logger.debug(
            f'{Utils.classname(self)}: reloading configuration from {self._configuration_location_finder.state()}'
        )

        raw_configuration = self._configuration_loader.load_if_exists(source)
        return self._event_dispatcher.dispatch([HQEvent.STATE_LOADED], HQState(
            federation=Federation.from_dict(raw_configuration.get('federation')),
            interfaces=WireguardConfiguration.from_dict_of_dicts(raw_configuration.get('interfaces')),
            forums=WireguardConfiguration.from_dict_of_dicts(raw_configuration.get('forums')),
            phone_lines=WireguardConfiguration.from_dict_of_dicts(raw_configuration.get('phone_lines')),
        ))

    def _generate_new_hq_state(self) -> HQState:
        self.__check_passphrase_retrieval_method()

        forum_key_pairs = self._wireguard_key_generator.generate_key_pairs()
        phone_line_key_pairs = self._wireguard_key_generator.generate_key_pairs()
        interface_key_pairs = self._wireguard_key_generator.generate_key_pairs()
        federation = self._event_dispatcher.dispatch(
            [HQEvent.FEDERATION_BEFORE_CREATE], Federation(name='wg-federation0')
        )

        return HQState(
            federation=federation,
            forums={
                'wgf-forum0': self._event_dispatcher.dispatch(
                    [HQEvent.FORUMS_CONFIGURATION_BEFORE_CREATE],
                    WireguardConfiguration(
                        interface=WireguardInterface(
                            address=('172.32.0.1/22',),
                            private_key=forum_key_pairs[0],
                            public_key=forum_key_pairs[1],
                            listen_port=federation.forum_min_port,
                            private_key_retrieval_method=self._user_input.private_key_retrieval_method,
                            post_up=self.__add_secret_retrieval_to_post_up((), 'forums', 'wgf-forum0')
                        ),
                        name='wgf-forum0',
                        kind=InterfaceKind.FORUM,
                        shared_psk=self._wireguard_key_generator.generate_psk(),
                        path=self.__real_path(
                            self._configuration_location_finder.forums_directory(), 'wgf-forum0'
                        )
                    )
                ),
            },

            phone_lines={
                'wgf-phoneline0': self._event_dispatcher.dispatch(
                    [HQEvent.PHONE_LINES_CONFIGURATION_BEFORE_CREATE],
                    WireguardConfiguration(
                        interface=WireguardInterface(
                            address=('172.32.4.1/22',),
                            private_key=phone_line_key_pairs[0],
                            public_key=phone_line_key_pairs[1],
                            listen_port=federation.phone_line_min_port,
                            private_key_retrieval_method=self._user_input.private_key_retrieval_method,
                            post_up=self.__add_secret_retrieval_to_post_up((), 'phone_lines', 'wgf-phoneline0')
                        ),
                        name='wgf-phoneline0',
                        kind=InterfaceKind.PHONE_LINE,
                        shared_psk=self._wireguard_key_generator.generate_psk(),
                        path=self.__real_path(
                            self._configuration_location_finder.phone_lines_directory(), 'wgf-phoneline0'
                        ),
                    )
                )
            },

            interfaces={
                'wg-federation0': self._event_dispatcher.dispatch(
                    [HQEvent.INTERFACES_CONFIGURATION_BEFORE_CREATE],
                    WireguardConfiguration(
                        interface=WireguardInterface(
                            address=('172.30.8.1/22',),
                            private_key=interface_key_pairs[0],
                            public_key=interface_key_pairs[1],
                            private_key_retrieval_method=self._user_input.private_key_retrieval_method,
                            post_up=self.__add_secret_retrieval_to_post_up((), 'interfaces', 'wg-federation0'),
                        ),
                        name='wg-federation0',
                        kind=InterfaceKind.INTERFACE,
                        shared_psk=self._wireguard_key_generator.generate_psk(),
                        path=self.__real_path(
                            self._configuration_location_finder.interfaces_directory(), 'wg-federation0'
                        ),
                    )
                ),
            },
        )

    def __check_passphrase_retrieval_method(self) -> None:
        if self.__should_use_insecure_private_key(self._user_input.private_key_retrieval_method):
            self._logger.warning(
                f'The root passphrase retrieval method has been set to '
                f'“{SecretRetrievalMethod.TEST_INSECURE_CLEARTEXT.value}”. '
                f'This is insecure: any user able to read configuration files would be able to get the private keys. '
                f'This method is left for testing purpose but SHOULD NOT be used in production.'
            )

    def __add_secret_retrieval_to_post_up(
            self, post_up: tuple[str, ...], interface_kind: str, interface_name: str
    ) -> tuple[str, ...]:
        if not self.__should_use_insecure_private_key(self._user_input.private_key_retrieval_method):
            post_up += (
                f'wg set %i private-key <(WG_FEDERATION_DEBUG=False wg-federation hq get-private-key '
                f'--interface-kind {interface_kind} '
                f'--interface-name {interface_name}'
                f'{self.__get_root_passphrase(self._user_input.private_key_retrieval_method, self._user_input.root_passphrase_command)}'
                f')',
            )

        return post_up

    def __get_root_passphrase(
            self, private_key_retrieval_method: SecretRetrievalMethod, root_passphrase_command: str
    ) -> str:
        if private_key_retrieval_method is SecretRetrievalMethod.WG_FEDERATION_COMMAND:
            return f' --root-passphrase-command "{root_passphrase_command}"'

        return ''

    def __should_use_insecure_private_key(self, private_key_retrieval_method: SecretRetrievalMethod) -> bool:
        return private_key_retrieval_method is SecretRetrievalMethod.TEST_INSECURE_CLEARTEXT

    def __real_path(self, directory: str, interface_name: str) -> str:
        return os.path.join(directory, f'{interface_name}.conf')

    def __dispatch_configuration_events(
            self, wg_configurations: Mapping[str, WireguardConfiguration], event: Enum
    ) -> None:
        for wg_configuration in wg_configurations.values():
            self._event_dispatcher.dispatch([event], wg_configuration)
