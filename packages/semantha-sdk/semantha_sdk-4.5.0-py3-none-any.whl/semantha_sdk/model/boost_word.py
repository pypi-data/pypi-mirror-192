from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from semantha_sdk.model.semantha_entity import SemanthaModelEntity


@dataclass(frozen=True)
class Boostword(SemanthaModelEntity):
    id: str
    word: Optional[str]
    regex: Optional[str]
    tags: list[str]


@dataclass(frozen=True)
class Boostwords(SemanthaModelEntity):
    _boostwords: list[Boostword]

    @property
    def boostwords(self) -> list[Boostword]:
        return self._boostwords
