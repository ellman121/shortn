# Shortnr - Python FastAPI built url shortener

## Notes

I've never used FastAPI before and I'm not a python professional, so expect some things to be non-conventional.

### How to run this

I'm assuming the user has postgres running with a DB called `shortn` already there.  No tables need to exist already though.

```bash
pip install -r deps
uvicorn main:app --reload
```

This will start a server on the local machine port `8000`.  You can interact with it via `curl` or Postman or whatever you're into.

### How to run tests

```bash
python -m unittest -v tests 
```

### File Structure

- `main.py` includes the routes being served
- `classes.py` includes shared class definitions (no real code)
- `db.py` is the database initialization stuff
- `url_shortener.py` includes implmentations for the routes
- `short_url_store.py` is the database implementation/abstraction layer

### Notes in the "real world"

- Let's just pretend that the DB username/password/URL are stored in a secret store or something... Felt beyond the scope of this challenge
- You wouldn't want to have one DB connection per request (especially in high traffic scenarios). I just did that here because I felt like the infrastructure to build/maintain shared connections was beyond the scope of this coding challenge and also I'm not sure how to do it off hand.
- All the DB initialization wouldn't be done as I have it here, but for completeness of a coding exercise, I am showing it all here.
- I wrote this using raw SQL but you would ideally use some kind of ORM to make your queries more stable and easier to read
- You would do a lot more tracking of request IDs / auth / etc., but I've skipped all that here since it felt beyond the scope of the exercise
- I'm generating the random shortcodes in python, but intelligent people can disagree about (a) when is best to do it and (b) where in the codebase.
