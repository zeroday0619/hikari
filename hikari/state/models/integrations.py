#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright © Nekoka.tt 2019
#
# This file is part of Hikari.
#
# Hikari is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Hikari is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Hikari. If not, see <https://www.gnu.org/licenses/>.
"""
Account integrations.
"""
from __future__ import annotations

import datetime

from hikari.state import state_registry
from hikari.state.models import interfaces
from hikari.state.models import users
from hikari.internal_utilities import auto_repr
from hikari.internal_utilities import date_helpers


class IntegrationAccount(interfaces.IStateful, interfaces.ISnowflake):
    """
    An account used for an integration.
    """

    __slots__ = ("_state", "id", "name")

    _state: state_registry.IStateRegistry

    #: The id for the account
    #:
    #: :type: :class:`int`
    id: int

    #: The name of the account
    #:
    #: :type: :class:`str`
    name: str

    __repr__ = auto_repr.repr_of("id", "name")

    def __init__(self, global_state: state_registry.IStateRegistry, payload):
        self._state = global_state
        self.id = int(payload["id"])
        self.name = payload.get("name")


class Integration(interfaces.IStateful, interfaces.ISnowflake):
    """
    A guild integration.
    """

    __slots__ = (
        "_state",
        "id",
        "name",
        "type",
        "enabled",
        "syncing",
        "_role_id",
        "expire_grace_period",
        "user",
        "account",
        "synced_at",
    )

    _state: state_registry.IStateRegistry
    _role_id: int

    #: The integration ID
    #:
    #: :type: :class:`int`
    id: int

    #: The name of the integration
    #:
    #: :type: :class:`str`
    name: str

    #: The type of integration (e.g. twitch, youtube, etc)
    #:
    #: :type: :class:`str`
    type: str

    #: Whether the integration is enabled or not.
    #:
    #: :type: :class:`bool`
    enabled: bool

    #: Whether the integration is currently synchronizing.
    #:
    #: :type: :class:`bool`
    syncing: bool

    #: The grace period for expiring subscribers.
    #:
    #: :type: :class:`int`
    expire_grace_period: int

    #: The user for this integration
    #:
    #: :type: :class:`hikari.core.models.users.User`
    user: users.User

    #: Integration account information.
    #:
    #: :type: :class:`hikari.core.models.integrations.IntegrationAccount`
    account: IntegrationAccount

    #: The time when the integration last synchronized.
    #:
    #: :type: :class:`datetime.datetime`
    synced_at: datetime.datetime

    __repr__ = auto_repr.repr_of("id", "name")

    def __init__(self, global_state: state_registry.IStateRegistry, payload):
        self._state = global_state
        self.id = int(payload["id"])
        self.name = payload["name"]
        self.type = payload["type"]
        self.enabled = payload["enabled"]
        self.syncing = payload["syncing"]
        self._role_id = int(payload["role_id"])
        self.expire_grace_period = int(payload["expire_grace_period"])
        self.user = global_state.parse_user(payload["user"])
        self.account = IntegrationAccount(global_state, payload["account"])
        self.synced_at = date_helpers.parse_iso_8601_ts(payload["synced_at"])


__all__ = ["Integration", "IntegrationAccount"]