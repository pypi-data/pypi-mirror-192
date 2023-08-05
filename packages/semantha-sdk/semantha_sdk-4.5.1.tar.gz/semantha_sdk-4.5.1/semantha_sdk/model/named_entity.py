from dataclasses import dataclass

from semantha_sdk.model.semantha_entity import SemanthaModelEntity


@dataclass(frozen=True)
class NamedEntity(SemanthaModelEntity):
    name: str
    text: str


@dataclass(frozen=True)
class NamedEntities(SemanthaModelEntity):

    def __post_init__(self):
        assert type(self.data) is list

    def __getitem__(self, index) -> NamedEntity:
        return NamedEntity(self.data[index])
