from typing import List
from beanie import Document
from pydantic import Extra
from bson import ObjectId

from constants.enum import Gender


class User(Document):
    name: str
    email: str
    password: str
    gender: Gender

    class Settings:
        name = 'users'

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        extra = Extra.forbid
