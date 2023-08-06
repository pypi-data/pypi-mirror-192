from marshmallow import fields

from semantha_sdk.model.document_metadata import DocumentMetadata
from semantha_sdk.model.semantha_entity import SemanthaSchema, with_entity


class DocumentMetadataSchema(SemanthaSchema, with_entity(DocumentMetadata)):
    file_name = fields.Str(
        data_key="fileName",
        required=True
    )
    document_type = fields.Str(
        data_key="documentType",
        required=True
    )
