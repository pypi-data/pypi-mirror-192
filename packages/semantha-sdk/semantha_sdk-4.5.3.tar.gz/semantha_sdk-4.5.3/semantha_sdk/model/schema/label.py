from marshmallow import fields

from semantha_sdk.model.label import Label
from semantha_sdk.model.semantha_entity import SemanthaSchema, with_entity


class LabelSchema(SemanthaSchema, with_entity(Label)):
    lang = fields.Str(
        data_key="lang",
        required=True
    )
    value = fields.Str(
        data_key="value",
        required=True
    )
