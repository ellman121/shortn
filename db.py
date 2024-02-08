from sqlalchemy import create_engine

# See Notes in Readme
DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/shortn"
db_engine = create_engine(DATABASE_URL)
