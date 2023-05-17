from pydantic import BaseModel, Extra
from bson import ObjectId
from typing import List


class Translate(BaseModel):
    language: str
    value: str

    # class Config:
    #     allow_population_by_field_name = True
    #     arbitrary_types_allowed = True
    #     json_encoders = {ObjectId: str}
    #     extra = Extra.forbid


class Comment(BaseModel):
    id: str
    content: str


class CommentTrans(object):
    id: str
    contentTrans: str

    def __init__(self, id, contentTrans):
        self.id = id
        self.contentTrans = contentTrans


class UserProfileTag(BaseModel):
    tags: List[str]
