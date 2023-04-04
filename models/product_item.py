from typing import List, Optional
from beanie import Document, Link
from pydantic import Field, Extra, BaseModel
from bson import ObjectId
from .variation_option import VariationOption
from .tag import Tag


class ProductItem(Document):
    price: int
    quantity: int
    thumbnail: str
    images: List[str]
    productConfigurations: Optional[List[Link[VariationOption]]]
    tags: List[Link[Tag]]

    class Settings:
        name = 'productitems'

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        extra = Extra.forbid


class ProdItemTag:
    def __init__(self, id: str, tags: List[str]):
        self.id = id
        self.tags = tags
