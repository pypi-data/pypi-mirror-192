from marshmallow import fields

from semantha_sdk.model.domain_configuration import DomainConfiguration
from semantha_sdk.model.schema.domain_setting import DomainSettingsSchema
from semantha_sdk.model.semantha_entity import SemanthaSchema, with_entity


class DomainConfigurationSchema(SemanthaSchema, with_entity(DomainConfiguration)):
    id = fields.Str(
        data_key="id",
        required=True
    )
    name = fields.Str(
        data_key="name",
        required=True
    )
    settings = fields.Nested(
        nested=DomainSettingsSchema(),
        data_key="settings",
        required=True
    )
