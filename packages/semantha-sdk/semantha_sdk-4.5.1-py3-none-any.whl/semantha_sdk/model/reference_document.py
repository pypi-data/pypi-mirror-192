from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from semantha_sdk.model.entity import Entity
from semantha_sdk.model.semantha_entity import SemanthaModelEntity


@dataclass(frozen=True)
class Parameters(SemanthaModelEntity):
    domain: str
    limit: Optional[int]
    offset: Optional[int]
    sort_by: Optional[str]
    return_fields: Optional[str]
    filter_document_class_ids: Optional[str]
    filter_name: Optional[str]
    filter_created_before: Optional[int]
    filter_created_after: Optional[int]
    filter_metadata: Optional[str]
    filter_comment: Optional[str]


@dataclass(frozen=True)
class MetaInfoPage(SemanthaModelEntity):
    range_from: int
    range_to: int
    range_total: int


@dataclass(frozen=True)
class Meta(SemanthaModelEntity):
    parameters: Parameters
    info: Optional[str]
    warnings: Optional[list[str]]
    page: MetaInfoPage


@dataclass(frozen=True)
class DocumentInformation(SemanthaModelEntity):
    # TODO: make all (?) properties optional since they might not be present if we use return fields parameter in
    #       reference documents get_all()
    id: str
    name: str
    tags: list[str]
    metadata: str
    filename: str
    created: int
    updated: int
    processed: int
    lang: Optional[str]
    content: Optional[str]
    document_class: Optional[Entity]
    derived_tags: list[str]
    color: Optional[str]
    derived_color: Optional[str]
    comment: Optional[str]
    derived_comment: Optional[str]


@dataclass(frozen=True)
class DocsPerTag(SemanthaModelEntity):
    tag: str
    count: int


@dataclass(frozen=True)
class Statistic(SemanthaModelEntity):
    library_size: int
    size: int
    number_of_sentences: int
    docs_per_tag: list[DocsPerTag]


@dataclass(frozen=True)
class ReferenceDocuments(SemanthaModelEntity):
    meta: Meta
    documents: list[DocumentInformation]
