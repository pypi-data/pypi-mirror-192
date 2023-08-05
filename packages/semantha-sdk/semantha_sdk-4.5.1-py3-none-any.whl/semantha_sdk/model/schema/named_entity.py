from marshmallow import fields

from semantha_sdk.model.named_entity import NamedEntity
from semantha_sdk.model.semantha_entity import SemanthaSchema, with_entity


class NamedEntitySchema(SemanthaSchema, with_entity(NamedEntity)):
    name = fields.Str(
        data_key="name",
        required=True
    )
    text = fields.Str(
        data_key="text",
        required=True
    )
