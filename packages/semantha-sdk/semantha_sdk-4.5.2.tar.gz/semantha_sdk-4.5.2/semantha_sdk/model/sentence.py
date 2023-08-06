from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from semantha_sdk.model.named_entity import NamedEntity
from semantha_sdk.model.reference import Reference
from semantha_sdk.model.semantha_entity import SemanthaModelEntity


@dataclass(frozen=True)
class Sentence(SemanthaModelEntity):
    id: str
    text: str
    document_name: Optional[str]
    named_entities: Optional[list[NamedEntity]]
    references: Optional[list[Reference]]