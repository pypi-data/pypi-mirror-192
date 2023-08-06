from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from semantha_sdk.model.paragraph import Paragraph
from semantha_sdk.model.semantha_entity import SemanthaModelEntity


@dataclass(frozen=True)
class PageContent(SemanthaModelEntity):
    paragraphs: Optional[list[Paragraph]]


@dataclass(frozen=True)
class Page(SemanthaModelEntity):
    contents: list[PageContent]
