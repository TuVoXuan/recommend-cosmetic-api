from typing import List
from beanie import Document, Link
from .variation import Variation
from common import Translate

class VariationOption(Document):
    parentVariation: Link[Variation];
    value: List[Translate]

    class Settings:
        name='variationoptions'