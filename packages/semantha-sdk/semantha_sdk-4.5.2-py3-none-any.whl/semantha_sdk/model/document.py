from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from semantha_sdk.model.page import Page
from semantha_sdk.model.reference import Reference
from semantha_sdk.model.reference_document import DocumentInformation
from semantha_sdk.model.semantha_entity import SemanthaModelEntity


@dataclass(frozen=True)
class Document(DocumentInformation):
    pages: list[Page]
    references: Optional[list[Reference]]
    image_pages: Optional[str]


@dataclass(frozen=True)
class Documents(SemanthaModelEntity):
    documents: list[Document]
