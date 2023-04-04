from beanie import Document, Link
from pydantic import Extra
from bson import ObjectId

from .product_item import ProductItem


class OrderItem(Document):
    productItem: Link[ProductItem]
    price: int
    quantity: str

    class Settings:
        name = 'orderitems'

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        extra = Extra.forbid
