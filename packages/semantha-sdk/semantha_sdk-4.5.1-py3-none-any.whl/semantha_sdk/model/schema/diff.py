from marshmallow import fields

from semantha_sdk.model.diff import Diff
from semantha_sdk.model.semantha_entity import SemanthaSchema, with_entity


class DiffSchema(SemanthaSchema, with_entity(Diff)):
    operation = fields.Str(
        data_key="operation",
        required=True
    )
    text = fields.Str(
        data_key="text",
        required=True
    )
