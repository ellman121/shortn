# Shortnr - Python FastAPI built url shortener

## Notes

I've never used FastAPI before and I'm not a python professional, so expect some things to be non-conventional.

### File Structure

- `main.py` includes the routes being served
- `classes.py` includes shared class definitions (no real code)
- `url_shortener.py` includes implmentations for the routes
- `short_url_store.py` is the database implementation/abstraction layer

### Notes in the "real world"

- Let's just pretend that the DB username/password/URL are stored in a secret store or something... Felt beyond the scope of this challenge
- You wouldn't want to have one DB connection per request (especially in high traffic scenarios). I just did that here because I felt like the infrastructure to build/maintain shared connections was beyond the scope of this coding challenge and also I'm not sure how to do it off hand.
- All the DB initialization wouldn't be done as I have it here, but for completeness of a coding exercise, I am showing it all here.
- I wrote this using raw SQL but you would ideally use some kind of ORM to make your queries more stable and easier to read
