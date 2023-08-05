from marshmallow import fields, post_load

from semantha_sdk.model.document import Document
from semantha_sdk.model.schema.document_information import DocumentInformationSchema
from semantha_sdk.model.schema.page import PageSchema
from semantha_sdk.model.schema.reference import ReferenceSchema


class DocumentSchema(DocumentInformationSchema):
    pages = fields.Nested(
        nested=PageSchema,
        data_key="pages",
        required=True,
        many=True
    )
    references = fields.Nested(
        nested=ReferenceSchema,
        data_key="references",
        required=False,
        load_default=None,
        many=True
    )
    image_pages = fields.Str(
        data_key="imagePages",
        required=False,
        load_default=None
    )

    @post_load
    def make_object(self, in_data, **kwargs):
        return Document(**in_data)
