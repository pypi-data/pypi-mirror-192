from __future__ import annotations

from dataclasses import dataclass

from marshmallow import fields

from semantha_sdk.model.semantha_entity import SemanthaModelEntity


@dataclass(frozen=True)
class Domain(SemanthaModelEntity):
    id: str
    name: str
    base_url: str


@dataclass(frozen=True)
class Domains(SemanthaModelEntity):
    domains: list[Domain]