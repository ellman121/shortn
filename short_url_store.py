from datetime import datetime, timezone
from classes import ShortenedURL, URLStats

# For now I'm going to store things in memory, I'll set up
# a database later
SHORTENED_URL_STORE: dict[str, ShortenedURL] = {}
URL_STATS_STORE: dict[str, URLStats] = {}

class DuplicateShortcodeError(Exception):
    pass

class UnknownShortcodeError(Exception):
    pass

# Adds to the store and returns the shortened URL object
def add_url_to_store(item: ShortenedURL):
    if SHORTENED_URL_STORE.get(item.shortcode) is not None:
        raise DuplicateShortcodeError(f"Shortcode `{item.shortcode}` already exists")
    
    SHORTENED_URL_STORE[item.shortcode] = item
    URL_STATS_STORE[item.shortcode] = URLStats(
        created=datetime.now(timezone.utc).isoformat(),
        lastRedirect=None,
        redirectCount=0
    )

    return ShortenedURL

def get_url(shortcode: str):
    surl = SHORTENED_URL_STORE.get(shortcode)
    if surl is None:
        raise UnknownShortcodeError(f"Shortcode `{shortcode}` is not known")
    
    # I like the idea that the store should automatically track the stats.  It
    # is however debatable whether this should be a part of this method or if
    # we should provide a "increment stats" function, which the user can, for
    # example, call after returning the 302 to whoever called the API.
    return surl

