from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from semantha_sdk.model.semantha_entity import SemanthaModelEntity


@dataclass(frozen=True)
class Synonym(SemanthaModelEntity):
    id: str
    word: Optional[str]
    regex: Optional[str]
    synonym: str
    tags: list[str]
