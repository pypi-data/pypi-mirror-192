from dataclasses import dataclass

from semantha_sdk.model.domain_settings import DomainSettings
from semantha_sdk.model.semantha_entity import SemanthaModelEntity


@dataclass(frozen=True)
class DomainConfiguration(SemanthaModelEntity):
    id: str
    name: str
    settings: DomainSettings


