from dataclasses import dataclass

from semantha_sdk.model.semantha_entity import SemanthaModelEntity


@dataclass(frozen=True)
class Entity(SemanthaModelEntity):
    id: str
    name: str


