from __future__ import annotations

from typing import Protocol

from proexe.users.types import UserProtocol


class DynamicTableProtocol(Protocol):
    name: str
    description: str
    dynamic_fields: list[DynamicFieldProtocol]

    user: UserProtocol


class DynamicFieldProtocol(Protocol):
    name: str
    type: str

    class Type:
        NUMBER = "NUMBER"
        STRING = "STRING"
        BOOLEAN = "BOOLEAN"
