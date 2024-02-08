import url_shortener

from fastapi import FastAPI
from sqlalchemy import create_engine, text


# See Notes in Readme
DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/shortn"

app = FastAPI()
db_engine = create_engine(DATABASE_URL)

# See Notes in Readme
@app.on_event("startup")
def startup():
    with db_engine.connect() as conn:
        conn.execute(text("""CREATE TABLE IF NOT EXISTS public.short_urls (
                          shortcode char(6) NOT NULL UNIQUE,
                          referenced_url text
                          );"""))
        conn.execute(text("""CREATE TABLE IF NOT EXISTS public.stats (
                          shortcode char(6) NOT NULL UNIQUE,
                          redirect_count INT DEFAULT 0,
                          created timestamp DEFAULT CURRENT_TIMESTAMP,
                          last_redirect timestamp DEFAULT NULL
                          );"""))
        conn.commit()

        try:
            conn.execute(text("""INSERT INTO public.short_urls (shortcode, referenced_url)
                          VALUES ('abc123', 'https://google.com');"""))
            conn.execute(text("""INSERT INTO public.stats (shortcode)
                            VALUES ('abc123');"""))
            conn.commit()
        except:
            pass

@app.get("/")
def read_root():
    return "Hello world"

@app.post("/shorten")
def create_shortenedUrl(body: url_shortener.CreateRequestBody):
    with db_engine.connect() as conn:
        return url_shortener.create_short_url(conn, body=body)

@app.get("/{shortcode}")
def read_shortcode(shortcode: str):
    with db_engine.connect() as conn:
        return url_shortener.get_short_url(conn, shortcode=shortcode)

@app.get("/{shortcode}/stats")
def read_shortcode_stats(shortcode: str):
    with db_engine.connect() as conn:
        return url_shortener.get_stats(conn, shortcode=shortcode)
