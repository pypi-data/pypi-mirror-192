from abc import ABC
from dataclasses import dataclass
from typing import Union, Optional, Type

from marshmallow import Schema, post_load


@dataclass(frozen=True)
class SemanthaModelEntity(ABC):
    pass

def with_entity(cls: Type[SemanthaModelEntity]):
    class WithEntity:
        _entity_class = cls

    return WithEntity

class SemanthaSchema(Schema):
    @post_load
    def make_object(self, in_data, **kwargs):
        if hasattr(self, "_entity_class"):
            return self._entity_class(**in_data)