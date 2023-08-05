from marshmallow import fields

from semantha_sdk.model.schema.named_entity import NamedEntitySchema
from semantha_sdk.model.schema.reference import ReferenceSchema
from semantha_sdk.model.semantha_entity import SemanthaSchema, with_entity
from semantha_sdk.model.sentence import Sentence


class SentenceSchema(SemanthaSchema, with_entity(Sentence)):
    id = fields.Str(
        data_key="id",
        required=True
    )
    text = fields.Str(
        data_key="text",
        required=True
    )
    document_name = fields.Str(
        data_key="documentName",
        required=False,
        load_default=None
    )
    named_entities = fields.Nested(
        nested=NamedEntitySchema,
        data_key="namedEntities",
        required=False,
        many=True,
        load_default=None
    )
    references = fields.Nested(
        nested=ReferenceSchema,
        data_key="references",
        required=False,
        many=True,
        load_default=None
    )
