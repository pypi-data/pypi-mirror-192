from marshmallow import fields

from semantha_sdk.model.reference_document import Statistic
from semantha_sdk.model.schema.reference_document import DocsPerTagSchema
from semantha_sdk.model.semantha_entity import SemanthaSchema, with_entity


class StatisticSchema(SemanthaSchema, with_entity(Statistic)):
    library_size = fields.Int(
        data_key="librarySize",
        required=True
    )
    size = fields.Int(
        data_key="size",
        required=True
    )
    number_of_sentences = fields.Int(
        data_key="numberOfSentences",
        required=True
    )
    docs_per_tag = fields.Nested(
        nested=DocsPerTagSchema,
        data_key="docsPerTag",
        required=True,
        many=True
    )
