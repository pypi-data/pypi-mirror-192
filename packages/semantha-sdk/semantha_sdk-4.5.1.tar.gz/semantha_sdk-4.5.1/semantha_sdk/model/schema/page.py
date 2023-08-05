from marshmallow import fields

from semantha_sdk.model.page import PageContent, Page
from semantha_sdk.model.schema.paragraph import ParagraphSchema
from semantha_sdk.model.semantha_entity import SemanthaSchema, with_entity


class PageContentSchema(SemanthaSchema, with_entity(PageContent)):
    paragraphs = fields.Nested(
        nested=ParagraphSchema,
        data_key="paragraphs",
        required=True,
        many=True
    )


class PageSchema(SemanthaSchema, with_entity(Page)):
    contents = fields.Nested(
        nested=PageContentSchema,
        data_key="contents",
        required=True,
        many=True
    )
