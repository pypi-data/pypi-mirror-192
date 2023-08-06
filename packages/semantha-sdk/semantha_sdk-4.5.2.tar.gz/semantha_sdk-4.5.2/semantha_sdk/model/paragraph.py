from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from semantha_sdk.model.reference import Reference
from semantha_sdk.model.semantha_entity import SemanthaModelEntity
from semantha_sdk.model.sentence import Sentence


@dataclass(frozen=True)
class Paragraph(SemanthaModelEntity):
    id: str
    type: str
    text: str
    sentences: list[Sentence]
    document_name: Optional[str]
    references: Optional[list[Reference]]
    context: dict[str, str]
    comment: str

@dataclass(frozen=True)
class PatchParagraph(SemanthaModelEntity):
    id: Optional[str]
    type: Optional[str]
    text: Optional[str]
    sentences: Optional[list[Sentence]]
    document_name: Optional[Optional[str]]
    references: Optional[list[Reference]]
    context: Optional[dict[str, str]]
    comment: Optional[str]

