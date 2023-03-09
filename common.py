from pydantic import BaseModel, Extra
from bson import ObjectId


class Translate(BaseModel):
    language: str
    value: str

    # class Config:
    #     allow_population_by_field_name = True
    #     arbitrary_types_allowed = True
    #     json_encoders = {ObjectId: str}
    #     extra = Extra.forbid
        
    