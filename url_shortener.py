import re
import rstr
import short_url_store

from typing import Union
from pydantic import BaseModel
from urllib.parse import urlparse
from classes import ShortenedURL, UnknownShortcodeError, DuplicateShortcodeError
from fastapi import HTTPException, Response

SHORTCODE_REGEX = "[a-zA-Z0-9]{6}"

class CreateRequestBody(BaseModel):
    url: Union[str, None] = ""
    shortcode: Union[str, None]= None

def create_short_url(body: Union[CreateRequestBody, None]):
    if body is None:
        raise HTTPException(400, detail="Invalid request body")
    
    referenced_url = body.url
    if referenced_url is None:
        raise HTTPException(400, detail="URL not provided")

    # You would want to talk to the product team and get opinions on whether or
    # not we want to support "invalid" URLs and whatever the definition of "invalid""
    # would be in our use case.  For this challenge, I'm only requiring both a
    # scheme and a network location, everything else is optional
    parsedUrl = urlparse(referenced_url)
    if parsedUrl.scheme == "" or parsedUrl.netloc == "":
        raise HTTPException(400, detail=f"'{referenced_url}' is an invalid url. Please provide both scheme://net.loc")
    
    if body.shortcode is None:
        body.shortcode = rstr.xeger(SHORTCODE_REGEX)
    
    new_shortcode = body.shortcode

    if re.match(SHORTCODE_REGEX, new_shortcode) is None:
        raise HTTPException(412, detail=f"Shortcode `{new_shortcode}` is invalid. Please match the regex /{SHORTCODE_REGEX}/")

    surl = ShortenedURL(shortcode=new_shortcode, referenced_url=referenced_url)
    try:
        short_url_store.add_url_to_store(surl)
    except DuplicateShortcodeError:
        raise HTTPException(409, detail=f"Shortcode `{new_shortcode}` already in use")
    
    return { "shortcode": surl.shortcode }

def get_short_url(shortcode: str):
    try:
        surl = short_url_store.get_url_and_increment_stats(shortcode)
        return Response(status_code=302, headers={
            "Location": surl.referenced_url
        })
    except UnknownShortcodeError:
        raise HTTPException(404, detail=f"Shortcode `{shortcode}` not found")

def get_stats(shortcode: str):
    try:
        stats = short_url_store.get_url_stats(shortcode)
        return stats
    except UnknownShortcodeError:
        raise HTTPException(404, detail=f"Shortcode `{shortcode}` not found")
