from marshmallow import fields

from semantha_sdk.model.paragraph import Paragraph
from semantha_sdk.model.schema.reference import ReferenceSchema
from semantha_sdk.model.schema.sentence import SentenceSchema
from semantha_sdk.model.semantha_entity import SemanthaSchema, with_entity


class ParagraphSchema(SemanthaSchema, with_entity(Paragraph)):
    id = fields.Str(
        data_key="id",
        required=True
    )
    type = fields.Str(
        data_key="type",
        required=True
    )
    text = fields.Str(
        data_key="text",
        required=True
    )
    sentences = fields.Nested(
        nested=SentenceSchema,
        data_key="sentences",
        required=False,
        many=True,
        load_default=None
    )
    document_name = fields.Str(
        data_key="documentName",
        required=False,
        load_default=None
    )
    references = fields.Nested(
        nested=ReferenceSchema,
        data_key="references",
        required=False,
        many=True,
        load_default=None
    )
    context = fields.Dict(
        data_key="context",
        required=False,
        load_default=None
    )
    comment = fields.Str(
        data_key="comment",
        required=False,
        load_default=None
    )
