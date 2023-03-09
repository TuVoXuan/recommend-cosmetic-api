from beanie import Document
from pydantic import Extra
from bson import ObjectId

class Tag(Document):
    name: str;

    class Settings:
        name='tags'

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        extra = Extra.forbid