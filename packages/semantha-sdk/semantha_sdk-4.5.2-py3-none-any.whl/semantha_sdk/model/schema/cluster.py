from marshmallow import fields

from semantha_sdk.model.cluster import ClusteredParagraph, DocumentCluster, ParagraphCluster, ClusteredDocument
from semantha_sdk.model.semantha_entity import SemanthaSchema, with_entity


class ClusteredDocumentSchema(SemanthaSchema, with_entity(ClusteredDocument)):
    document_id = fields.Str(
        data_key="documentId",
        required=True
    )
    probability = fields.Float(
        data_key="probability",
        required=True
    )


class ClusteredParagraphSchema(SemanthaSchema, with_entity(ClusteredParagraph)):
    document_id = fields.Str(
        data_key="documentId",
        required=True
    )
    paragraph_id = fields.Str(
        data_key="paragraphId",
        required=True
    )
    probability = fields.Float(
        data_key="probability",
        required=True
    )


class DocumentClusterSchema(SemanthaSchema, with_entity(DocumentCluster)):
    id = fields.Int(
        data_key="id",
        required=True
    )
    count = fields.Int(
        data_key="count",
        required=True
    )
    label = fields.Str(
        data_key="label",
        required=True
    )
    content = fields.Nested(
        nested=ClusteredDocumentSchema,
        data_key="content",
        required=True,
        many=True
    )


class ParagraphClusterSchema(SemanthaSchema, with_entity(ParagraphCluster)):
    id = fields.Int(
        data_key="id",
        required=True
    )
    count = fields.Int(
        data_key="count",
        required=True
    )
    label = fields.Str(
        data_key="label",
        required=True
    )
    content = fields.Nested(
        nested=ClusteredParagraphSchema,
        data_key="content",
        required=True
    )
