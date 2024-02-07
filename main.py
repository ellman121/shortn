### Some Notes
# - This is my first itme using FastAPI, I figured I'd give it a spin during
#   the coding challenge.  I may do things non-conventionally as a result
# - I've organized the code with this file containing the router, a few "modules"
#   (probably the incorrect python terminology) containing route implementations
#   and other things, and a `classes` file for shared classes to avoid circular
#   imports. I'm sure there's a more 'pythonic' way of doing this, but that's
#   not something I'm a professional in
import url_shortener

from fastapi import FastAPI


app = FastAPI()

@app.get("/")
def read_root():
    return "Hello world"

@app.post("/shorten")
def create_shortenedUrl(body: url_shortener.CreateRequestBody):
    return url_shortener.create(body=body)

@app.get("/{shortcode}")
def read_shortcode(shortcode: str):
    return url_shortener.get(shortcode=shortcode)

@app.get("/{shortcode}/stats")
def read_shortcode_stats(shortcode: str):
    return f"You requested stats for {shortcode}"
