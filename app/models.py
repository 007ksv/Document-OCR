from pydantic import BaseModel, validator

from .utils import is_valid_url


class OCRDocument(BaseModel):
    image_url: str

    @validator("image_url")
    def is_valid(cls, value: str) -> bool:
        if not is_valid_url(value):
            raise ValueError("`image_url` is not a valid url")
        return value.strip()
