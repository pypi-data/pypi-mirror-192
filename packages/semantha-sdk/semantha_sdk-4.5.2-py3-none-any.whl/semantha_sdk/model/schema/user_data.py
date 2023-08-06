from marshmallow import fields

from semantha_sdk.model.semantha_entity import SemanthaSchema, with_entity
from semantha_sdk.model.user_data import UserData


class UserDataSchema(SemanthaSchema, with_entity(UserData)):
    name = fields.Str(
        data_key="name",
        required=True
    )
    valid_until = fields.Int(
        data_key="validUntil",
        required=True
    )
    roles = fields.List(
        cls_or_instance=fields.Str(),
        data_key="roles",
        required=True
    )
