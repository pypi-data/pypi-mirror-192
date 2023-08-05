from marshmallow import fields

from semantha_sdk.model.semantha_entity import SemanthaSchema, with_entity
from semantha_sdk.model.synonym import Synonym


class SynonymSchema(SemanthaSchema, with_entity(Synonym)):
    id = fields.Str(
        data_key="id",
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
    synonym = fields.Str(
        data_key="synonym",
        required=True
    )
    tags = fields.List(
        cls_or_instance=fields.Str(),
        data_key="tags",
        required=True
    )
