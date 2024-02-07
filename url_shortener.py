from fastapi import HTTPException
from typing import Union
from pydantic import BaseModel

from urllib.parse import urlparse

class RequestBody(BaseModel):
    url: str = ""
    shortcode: Union[str, None]= None

def create(body: RequestBody):
    if body is None:
        # Again, in the real would, you would track request IDs and stuff
        # for your support staff to use to track down what went wrong, but
        # not messing around with it for the coding challenge
        raise HTTPException(400, detail="Invalid request body")
    
    url = body.url
    if url is None:
        raise HTTPException(400, detail="URL not provided")

    # You would want to talk to the product team and get opinions on whether or
    # not we want to support "invalid" URLs and whatever the definition of "invalid""
    # would be in our use case.  For this challenge, I'm only requiring both a
    # scheme and a network location, everything else is optional
    parsedUrl = urlparse(url)
    if parsedUrl.scheme == "" or parsedUrl.netloc == "":
        raise HTTPException(400, detail=f"'{url}' is an invalid url.  Please provide both scheme://net.loc")
    
    
    return ""
