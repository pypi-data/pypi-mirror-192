from __future__ import annotations

from dataclasses import dataclass

from semantha_sdk.model.semantha_entity import SemanthaModelEntity


@dataclass(frozen=True)
class ClusteredDocument(SemanthaModelEntity):
    document_id: str
    probability: float


@dataclass(frozen=True)
class ClusteredParagraph(SemanthaModelEntity):
    document_id: str
    paragraph_id: str
    probability: float


@dataclass(frozen=True)
class DocumentCluster(SemanthaModelEntity):
    id: int
    count: int
    label: str
    content: list[ClusteredDocument]


@dataclass(frozen=True)
class ParagraphCluster(SemanthaModelEntity):
    id: int
    count: int
    label: str
    content: list[ClusteredParagraph]


@dataclass(frozen=True)
class DocumentClusters(SemanthaModelEntity):
    clusters: list[DocumentCluster]


@dataclass(frozen=True)
class ParagraphClusters(SemanthaModelEntity):
    clusters: list[ParagraphCluster]
