### Some Notes
# - This is my first itme using FastAPI, I figured I'd give it a spin during
#   the coding challenge.  I may do things non-conventionally as a result
# - I felt like buliding/integrating a Database was beyond the scope of the
#   challenge, so I am using an in-memory dictionary for URLs which have
#   already been shortened.

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return "Hello world"

@app.post("/shorten")
def create_shortenedUrl():
    return "TBD"

@app.get("/{shortcode}")
def read_shortcode(shortcode: str):
    return f"You requested {shortcode}"

@app.get("/{shortcode}/stats")
def read_shortcode_stats(shortcode: str):
    return f"You requested stats for {shortcode}"
