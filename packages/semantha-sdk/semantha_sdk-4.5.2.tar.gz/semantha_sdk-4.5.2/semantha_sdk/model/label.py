from dataclasses import dataclass

from semantha_sdk.model.semantha_entity import SemanthaModelEntity


@dataclass(frozen=True)
class Label(SemanthaModelEntity):
    lang: str
    value: str
