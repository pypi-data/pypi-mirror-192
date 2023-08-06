from marshmallow import fields

from semantha_sdk.model.boost_word import Boostword
from semantha_sdk.model.semantha_entity import SemanthaSchema, with_entity


class BoostwordSchema(SemanthaSchema, with_entity(Boostword)):
    id = fields.Str(
        data_key="id",
        required=True
    )
    tags = fields.List(
        cls_or_instance=fields.Str(),
        data_key="tags",
        required=True
    )
    word = fields.Str(
        data_key="word",
        load_default=None
    )
    regex = fields.Str(
        data_key="regex",
        load_default=None
    )
