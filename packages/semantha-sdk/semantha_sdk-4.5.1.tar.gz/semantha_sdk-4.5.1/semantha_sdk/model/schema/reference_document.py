from marshmallow import fields

from semantha_sdk.model.reference_document import ReferenceDocuments, Parameters, Meta, MetaInfoPage, \
    DocsPerTag
from semantha_sdk.model.schema.document_information import DocumentInformationSchema
from semantha_sdk.model.semantha_entity import SemanthaSchema, with_entity


class ParametersSchema(SemanthaSchema, with_entity(Parameters)):
    domain = fields.Str(
        data_key="domain",
        required=True
    )
    limit = fields.Int(
        data_key="limit",
        required=False,
        load_default=None
    )
    offset = fields.Int(
        data_key="offset",
        required=False,
        load_default=None
    )
    sort_by = fields.Str(
        data_key="sort",
        required=False,
        load_default=None
    )
    return_fields = fields.Str(
        data_key="fields",
        required=False,
        load_default=None
    )
    filter_document_class_ids = fields.Str(
        data_key="documentclassids",
        required=False,
        load_default=None
    )
    filter_name = fields.Str(
        data_key="name",
        required=False,
        load_default=None
    )
    filter_created_before = fields.Int(
        data_key="createdbefore",
        required=False,
        load_default=None
    )
    filter_created_after = fields.Int(
        data_key="createafter",
        required=False,
        load_default=None
    )
    filter_metadata = fields.Str(
        data_key="metadata",
        required=False,
        load_default=None
    )
    filter_comment = fields.Str(
        data_key="comment",
        required=False,
        load_default=None
    )


class MetaInfoPageSchema(SemanthaSchema, with_entity(MetaInfoPage)):
    range_from = fields.Int(
        data_key="from",
        required=True
    )
    range_to = fields.Int(
        data_key="to",
        required=True
    )
    range_total = fields.Int(
        data_key="total",
        required=True
    )


class MetaSchema(SemanthaSchema, with_entity(Meta)):
    parameters = fields.Nested(
        nested=ParametersSchema,
        data_key="parameters",
        required=True
    )
    info = fields.Str(
        data_key="info",
        required=False,
        load_default=None
    )
    warnings = fields.List(
        cls_or_instance=fields.Str(),
        data_key="warnings",
        required=False,
        load_default=None
    )
    page = fields.Nested(
        nested=MetaInfoPageSchema,
        data_key="page",
        required=False,
        load_default=None
    )


class DocsPerTagSchema(SemanthaSchema, with_entity(DocsPerTag)):
    tag = fields.Str(
        data_key="tag",
        required=True
    )
    count = fields.Int(
        data_key="count",
        required=True
    )


class ReferenceDocumentsSchema(SemanthaSchema, with_entity(ReferenceDocuments)):
    meta = fields.Nested(
        nested=MetaSchema,
        data_key="meta",
        required=True
    )
    documents = fields.Nested(
        nested=DocumentInformationSchema,
        data_key="data",
        required=True,
        many=True
    )
