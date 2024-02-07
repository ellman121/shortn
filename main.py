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
    return url_shortener.get_stats(shortcode=shortcode)
