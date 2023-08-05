from __future__ import annotations

from dataclasses import dataclass

from semantha_sdk.model.semantha_entity import SemanthaModelEntity


@dataclass(frozen=True)
class Diff(SemanthaModelEntity):
    operation: str
    text: str
