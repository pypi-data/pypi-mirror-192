from marshmallow import fields

from semantha_sdk.model.domain import Domain
from semantha_sdk.model.semantha_entity import SemanthaSchema, with_entity


class DomainSchema(SemanthaSchema, with_entity(Domain)):
    id = fields.Str(
        data_key="id",
        required=True
    )
    name = fields.Str(
        data_key="name",
        required=True
    )
    base_url = fields.Str(
        data_key="baseUrl",
        required=True
    )
