from marshmallow import fields

from semantha_sdk.model.entity import Entity
from semantha_sdk.model.semantha_entity import SemanthaSchema, with_entity


class EntitySchema(SemanthaSchema, with_entity(Entity)):
    id = fields.Str(
        data_key="id",
        required=True
    )
    name = fields.Str(
        data_key="name",
        required=True
    )
