from __future__ import annotations

from dataclasses import dataclass

from marshmallow import Schema, fields, post_load

from semantha_sdk.model.data_type import DataType
from semantha_sdk.model.label import Label
from semantha_sdk.model.metadata import Metadata
from semantha_sdk.model.semantha_entity import SemanthaModelEntity


@dataclass(frozen=True)
class Class(SemanthaModelEntity):
    id: str
    name: str
    read_only: bool
    functional: bool
    labels: list[Label]
    metadata: list[Metadata]
    comment: str
    datatype: DataType
    attribute_ids: list[str]
    relevant_for_relation: bool
    object_property_id: str
    parent_id: str

