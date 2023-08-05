from marshmallow import fields

from semantha_sdk.model.cls import Class
from semantha_sdk.model.data_type import DataType
from semantha_sdk.model.schema.label import LabelSchema
from semantha_sdk.model.schema.metadata import MetadataSchema
from semantha_sdk.model.semantha_entity import SemanthaSchema, with_entity


class ClassSchema(SemanthaSchema, with_entity(Class)):
    id = fields.Str(
        data_key="id",
        required=True
    )
    name = fields.Str(
        data_key="name",
        required=True
    )
    read_only = fields.Bool(
        data_key="readOnly",
        required=True
    )
    functional = fields.Bool(
        data_key="functional",
        required=True
    )
    labels = fields.Nested(
        nested=LabelSchema(),
        data_key="labels",
        required=True,
        many=True
    )
    metadata = fields.Nested(
        nested=MetadataSchema(),
        data_key="metadata",
        required=True,
        many=True
    )
    comment = fields.Str(
        data_key="comment",
        required=True
    )
    datatype = fields.Enum(
        enum=DataType,
        data_key="datatype",
        required=True
    )
    attribute_ids = fields.List(
        cls_or_instance=fields.Str(),
        data_key="attributeIds",
        required=True,
    )
    relevant_for_relation = fields.Bool(
        data_key="relevantForRelation",
        required=True
    )
    object_property_id = fields.Str(
        data_key="objectPropertyId",
        required=True
    )
    parent_id = fields.Str(
        data_key="parentId",
        required=True
    )
