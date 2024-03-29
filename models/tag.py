from typing import Optional
from beanie import Document, Link
from pydantic import Extra
from bson import ObjectId

from .tag_group import TagGroup


class Tag(Document):
    name: str
    weight: int
    parent: Link[TagGroup]

    class Settings:
        name = 'tags'

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        extra = Extra.forbid
