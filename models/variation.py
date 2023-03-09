from typing import List
from beanie import Document
from common import Translate

class Variation(Document):
    name: List[Translate];

    class Settings:
        name='variations'