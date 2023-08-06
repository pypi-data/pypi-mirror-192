from marshmallow import fields

from semantha_sdk.model.metadata import Metadata
from semantha_sdk.model.semantha_entity import with_entity, SemanthaSchema


class MetadataSchema(SemanthaSchema, with_entity(Metadata)):
    id = fields.Str(
        data_key="id",
        required=True
    )
    value = fields.Str(
        data_key="value",
        required=True
    )
