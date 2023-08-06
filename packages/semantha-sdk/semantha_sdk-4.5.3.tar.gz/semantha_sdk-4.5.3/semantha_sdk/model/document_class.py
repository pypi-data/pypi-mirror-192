from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from semantha_sdk.model.semantha_entity import SemanthaModelEntity


@dataclass(frozen=True)
class DocumentClass(SemanthaModelEntity):
    id: str
    name: str
    created: int
    updated: int
    documents_count: int
    parent_id: Optional[str]
    sub_classes: Optional[list[DocumentClass]]
    tags: Optional[list[str]]
    derived_tags: Optional[list[str]]
    color: Optional[str]
    comment: Optional[str]
    derived_comment: Optional[str]
    metadata: Optional[str]
    derived_metadata: Optional[str]

