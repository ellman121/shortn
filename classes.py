from typing import Union
from pydantic import BaseModel
from datetime import datetime


class ShortenedURL(BaseModel):
    shortcode: str
    referenced_url: str

class URLStats(BaseModel):
    created: datetime # ISO format datetime string
    lastRedirect: Union[datetime, None] # Again ISOFormat
    redirectCount: int

class DuplicateShortcodeError(Exception):
    pass

class UnknownShortcodeError(Exception):
    pass

class DBMismatchError(Exception):
    pass

class DBConnectionError(Exception):
    pass
