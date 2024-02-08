from classes import DuplicateShortcodeError, ShortenedURL, URLStats, UnknownShortcodeError, DBMismatchError
from sqlalchemy import text
from db import db_engine

# Adds to the store and returns the shortened URL object
def add_url_to_store(item: ShortenedURL):
    with db_engine.connect() as conn:
        shortcode = item.shortcode
        try:
            conn.execute(text(f"""INSERT INTO public.short_urls (shortcode, referenced_url)
                            VALUES ('{shortcode}', '{item.referenced_url}');"""))
            conn.execute(text(f"""INSERT INTO public.stats (shortcode) VALUES ('{shortcode}');"""))
        except:
            raise DuplicateShortcodeError(f"Shortcode `{item.shortcode}` already exists")

        conn.commit()
        return ShortenedURL

def get_url_and_increment_stats(shortcode: str):
    with db_engine.connect() as conn:
        query = conn.execute(text(f"""SELECT referenced_url FROM public.short_urls
                                    WHERE shortcode='{shortcode}'"""))
        row = query.first()
        if row is None:
            raise UnknownShortcodeError(f"Shortcode `{shortcode}` is not known")

        referenced_url = row[0]

        # I like the idea that the store class should track the stats. It is
        # however debatable whether this should be a part of this method or if
        # we should provide a "increment stats" function, which the can, for
        # example, be called after returning the 302.

        query = conn.execute(text(f"""SELECT redirect_count FROM public.stats
                                    WHERE shortcode='{shortcode}'"""))
        row = query.first()
        if row is None:
            raise DBMismatchError
        
        count = row[0]
        conn.execute(text(f"""UPDATE public.stats SET
                        redirect_count = {count + 1},
                        last_redirect = CURRENT_TIMESTAMP
                        WHERE shortcode='{shortcode}'"""))

        conn.commit()
        return ShortenedURL(shortcode=shortcode, referenced_url=referenced_url)

def get_url_stats(shortcode: str):
    with db_engine.connect() as conn:
        query = conn.execute(text(f"""SELECT created, last_redirect, redirect_count FROM public.stats
                                WHERE shortcode='{shortcode}'"""))
        row = query.first()
        if row is None:
            raise UnknownShortcodeError(f"Shortcode `{shortcode}` is not known")
        
        conn.commit()
        return URLStats(created=row[0], lastRedirect=row[1], redirectCount=row[2])
