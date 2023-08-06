from marshmallow import fields

from semantha_sdk.model.reference import Reference
from semantha_sdk.model.semantha_entity import with_entity, SemanthaSchema


class ReferenceSchema(SemanthaSchema, with_entity(Reference)):
    document_id = fields.Str(
        data_key="documentId",
        required=True
    )
    similarity = fields.Float(
        data_key="similarity",
        required=True
    )
    color = fields.Str(
        data_key="color",
        required=True
    )
    document_name = fields.Str(
        data_key="documentName",
        required=False,
        load_default=None
    )
    page_number = fields.Int(
        data_key="pageNumber",
        required=False,
        load_default=None
    )
    paragraph_id = fields.Str(
        data_key="paragraphId",
        required=False,
        load_default=None
    )
    sentence_id = fields.Str(
        data_key="sentenceId",
        required=False,
        load_default=None
    )
    text = fields.Str(
        data_key="text",
        required=False,
        load_default=None
    )
    context = fields.Dict(
        data_key="context",
        required=False,
        load_default=None
    )
    type = fields.Str(
        data_key="type",
        required=False,
        load_default=None
    )
    comment = fields.Str(
        data_key="comment",
        required=False,
        load_default=None
    )
    has_opposite_meaning = fields.Bool(
        data_key="hasOppositeMeaning",
        required=False,
        load_default=None
    )
