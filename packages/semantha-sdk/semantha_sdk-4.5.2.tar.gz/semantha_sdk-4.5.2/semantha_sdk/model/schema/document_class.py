from marshmallow import fields

from semantha_sdk.model.document_class import DocumentClass
from semantha_sdk.model.semantha_entity import SemanthaSchema, with_entity


class DocumentClassSchema(SemanthaSchema, with_entity(DocumentClass)):
    id = fields.Str(
        data_key="id",
        required=True
    )
    name = fields.Str(
        data_key="name",
        required=True
    )
    created = fields.Int(
        data_key="created",
        required=False,
        load_default=None
    )
    updated = fields.Int(
        data_key="updated",
        required=False,
        load_default=None
    )
    documents_count = fields.Int(
        data_key="documentsCount",
        required=False,
        load_default=None
    )
    parent_id = fields.Str(
        data_key="parentId",
        required=False,
        load_default=None
    )
    sub_classes = fields.Nested(
        nested=lambda: DocumentClassSchema,
        data_key="subClasses",
        required=False,
        many=True,
        load_default=None
    )
    tags = fields.List(
        cls_or_instance=fields.Str(),
        data_key="tags",
        required=False,
        load_default=None
    )
    derived_tags = fields.List(
        cls_or_instance=fields.Str(),
        data_key="derivedTags",
        required=False,
        load_default=None
    )
    color = fields.Str(
        data_key="color",
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
    metadata = fields.Str(
        data_key="metadata",
        required=False,
        load_default=None
    )
    derived_metadata = fields.Str(
        data_key="derivedMetadata",
        required=False,
        load_default=None
    )
