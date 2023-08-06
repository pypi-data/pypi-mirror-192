from enum import Enum
from typing import Optional

from wg_federation.data.state.federation import Federation
from wg_federation.data.state.hq_state import HQState
from wg_federation.data.state.wireguard_configuration import WireguardConfiguration


class HQEvent(tuple[str, type, Optional[bool]], Enum):
    """
    HQ events
    """

    BOOTSTRAPPED = ('bootstrapped', HQState)

    FEDERATION_LOADED = ('federation_loaded', Federation)
    FEDERATION_BEFORE_CREATE = ('federation_before_create', Federation, True)
    FEDERATION_CREATED = ('federation_created', Federation)
    FEDERATION_BEFORE_UPDATE = ('federation_before_update', Federation, True)
    FEDERATION_UPDATED = ('federation_updated', Federation)
    FEDERATION_BEFORE_DELETE = ('federation_before_delete', Federation, True)
    FEDERATION_DELETED = ('federation_before_delete', Federation)

    INTERFACES_CONFIGURATION_BEFORE_CREATE = ('interface_before_create', WireguardConfiguration, True)
    INTERFACES_CONFIGURATION_CREATED = ('interface_created', WireguardConfiguration)
    INTERFACES_CONFIGURATION_BEFORE_UPDATE = ('interface_before_update', WireguardConfiguration, True)
    INTERFACES_CONFIGURATION_UPDATED = ('interface_updated', WireguardConfiguration)
    INTERFACES_CONFIGURATION_BEFORE_DELETE = ('interface_before_delete', WireguardConfiguration, True)
    INTERFACES_CONFIGURATION_DELETED = ('interface_deleted', WireguardConfiguration)

    FORUMS_CONFIGURATION_BEFORE_CREATE = ('forum_before_create', WireguardConfiguration, True)
    FORUMS_CONFIGURATION_CREATED = ('forum_created', WireguardConfiguration)
    FORUMS_CONFIGURATION_BEFORE_UPDATE = ('forum_before_update', WireguardConfiguration, True)
    FORUMS_CONFIGURATION_UPDATED = ('forum_updated', WireguardConfiguration)
    FORUMS_CONFIGURATION_BEFORE_DELETE = ('forum_before_delete', WireguardConfiguration, True)
    FORUMS_CONFIGURATION_DELETED = ('forum_deleted', WireguardConfiguration)

    PHONE_LINES_CONFIGURATION_BEFORE_CREATE = ('phone_line_before_create', WireguardConfiguration, True)
    PHONE_LINES_CONFIGURATION_CREATED = ('phone_line_created', WireguardConfiguration)
    PHONE_LINES_CONFIGURATION_BEFORE_UPDATE = ('phone_line_before_update', WireguardConfiguration, True)
    PHONE_LINES_CONFIGURATION_UPDATED = ('phone_line_updated', WireguardConfiguration)
    PHONE_LINES_CONFIGURATION_BEFORE_DELETE = ('phone_line_before_delete', WireguardConfiguration, True)
    PHONE_LINES_CONFIGURATION_DELETED = ('phone_line_deleted', WireguardConfiguration)

    STATE_LOADED = ('state_loaded', HQState)
    STATE_BEFORE_CREATE = ('state_before_create', HQState)
    STATE_CREATED = ('state_created', HQState)
    STATE_BEFORE_UPDATE = ('state_before_update', HQState, True)
    STATE_UPDATED = ('state_updated', HQState)

    @classmethod
    def dynamic_get(cls, kind: str, value: str) -> 'HQEvent':
        """
        Dynamically search for HQEvent enum value of kind, with value.
        For example, cls.dynamic_get('forums', 'CONFIGURATION_BEFORE_CREATE').
        :param kind:
        :param value:
        :return:
        """
        return getattr(cls, f'{kind.upper()}_{value}')
