from __future__ import annotations

from dataclasses import dataclass

from marshmallow import fields

from semantha_sdk.model.semantha_entity import SemanthaModelEntity


@dataclass(frozen=True)
class UserData(SemanthaModelEntity):
    name: str
    valid_until: int
    roles: list[str]



