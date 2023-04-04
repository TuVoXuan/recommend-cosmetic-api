from beanie import Document, Link
from pydantic import Extra
from bson import ObjectId
from pydantic import BaseModel

from .order_item import OrderItem


class Comment(Document):
    content: str
    user: str
    rate: int
    orderItem: Link[OrderItem]

    class Settings:
        name = 'comments'

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        extra = Extra.forbid


class OutputComment:
    def __init__(self,  user: str, rate: int, productItem: str) -> None:
        self.user = user
        self.rate = rate
        self.productItem = productItem

    def to_dict(self):
        return {
            'userId': self.user,
            'itemId': self.productItem,
            'rating': self.rate
        }
