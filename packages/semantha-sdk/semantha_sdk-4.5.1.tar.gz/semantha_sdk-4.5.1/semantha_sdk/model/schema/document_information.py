from marshmallow import fields

from semantha_sdk.model.reference_document import DocumentInformation
from semantha_sdk.model.schema.entity import EntitySchema
from semantha_sdk.model.semantha_entity import SemanthaSchema, with_entity


class DocumentInformationSchema(SemanthaSchema, with_entity(DocumentInformation)):
    id = fields.Str(
        data_key="id",
        required=True
    )
    name = fields.Str(
        data_key="name",
        required=True
    )
    tags = fields.List(
        cls_or_instance=fields.Str(),
        data_key="tags",
        required=True
    )
    metadata = fields.Str(
        data_key="metadata",
        required=False,
        load_default=None
    )
    filename = fields.Str(
        data_key="filename",
        required=True
    )
    created = fields.Int(
        data_key="created",
        required=True
    )
    updated = fields.Int(
        data_key="updated",
        required=True
    )
    processed = fields.Bool(
        data_key="processed",
        required=True
    )
    lang = fields.Str(
        data_key="lang",
        required=False,
        load_default=None
    )
    content = fields.Str(
        data_key="content",
        required=False,
        load_default=None
    )
    document_class = fields.Nested(
        nested=EntitySchema(),
        data_key="documentClass",
        required=False,
        load_default=None
    )
    derived_tags = fields.List(
        cls_or_instance=fields.Str(),
        data_key="derivedTags",
        required=True
    )
    color = fields.Str(
        data_key="color",
        required=False,
        load_default=None
    )
    derived_color = fields.Str(
        data_key="derived_color",
        required=False,
        load_default=None
    )
    comment = fields.Str(
        data_key="comment",
        required=False,
        load_default=None
    )
    derived_comment = fields.Str(
        data_key="derivedComment",
        required=False,
        load_default=None
    )
