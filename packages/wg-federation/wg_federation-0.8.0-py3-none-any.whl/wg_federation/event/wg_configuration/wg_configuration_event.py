from enum import Enum
from typing import Optional

from wg_federation.data.state.wireguard_configuration import WireguardConfiguration


class WGConfigurationEvent(tuple[str, type, Optional[bool]], Enum):
    """
    WGConfiguration events
    """

    CONFIGURATION_FILE_LOADED = ('conf_file_loaded', WireguardConfiguration, True)
    CONFIGURATION_FILE_BEFORE_CREATE = ('conf_file_before_create', WireguardConfiguration, True)
    CONFIGURATION_FILE_CREATED = ('conf_file_created', WireguardConfiguration, True)
    CONFIGURATION_FILE_BEFORE_UPDATE = ('conf_file_before_update', WireguardConfiguration, True)
    CONFIGURATION_FILE_UPDATED = ('conf_file_updated', WireguardConfiguration, True)
    CONFIGURATION_FILE_BEFORE_DELETE = ('conf_file_before_delete', WireguardConfiguration, True)
    CONFIGURATION_FILE_DELETED = ('conf_file_before_delete', WireguardConfiguration, True)
