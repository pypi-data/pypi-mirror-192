from dataclasses import dataclass

from semantha_sdk.model.semantha_entity import SemanthaModelEntity


@dataclass(frozen=True)
class DocumentMetadata(SemanthaModelEntity):
    file_name: str
    document_type: str
