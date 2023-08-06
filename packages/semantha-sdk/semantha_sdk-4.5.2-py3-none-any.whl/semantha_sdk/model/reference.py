from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from semantha_sdk.model.semantha_entity import SemanthaModelEntity


@dataclass(frozen=True)
class Reference(SemanthaModelEntity):
    document_id: str
    similarity: float
    color: str
    document_name: Optional[str]
    page_number: Optional[int]
    paragraph_id: Optional[int]
    sentence_id: Optional[str]
    text: Optional[str]
    context: Optional[dict[str, str]]
    type: Optional[str]
    comment: Optional[str]
    has_opposite_meaning: Optional[bool]



