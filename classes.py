from typing import Union
from pydantic import BaseModel


class ShortenedURL(BaseModel):
    shortcode: str
    referenced_url: str

class URLStats(BaseModel):
    created: str # ISO format datetime string
    lastRedirect: Union[str, None] # Again ISOFormat
    redirectCount: int
