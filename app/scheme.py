import pydantic
from typing import Optional, Type


class AbstractAdv(pydantic.BaseModel):
    title: str
    description: str
    user_id: int

    @pydantic.field_validator("title")
    @classmethod
    def title_length(cls, text: str) -> str:
        if len(text) > 50:
            raise ValueError('invalid number of characters (>50)')
        if len(text) == 0:
            raise ValueError('field "title" cannot be empty')
        return text

    @pydantic.field_validator("description")
    @classmethod
    def description_length(cls, text: str) -> str:
        if len(text) > 50:
            raise ValueError('invalid number of characters (>200)')
        if len(text) == 0:
            raise ValueError('field "description" cannot be empty')
        return text


class CreateAdv(AbstractAdv):
    title: str
    description: str
    user_id: int


class UpdateAdv(AbstractAdv):
    title: Optional[str] = None
    description: Optional[str] = None
    user_id: Optional[int] = None


SCHEMA_CLASS = Type[CreateAdv | UpdateAdv]
SCHEMA = CreateAdv | UpdateAdv