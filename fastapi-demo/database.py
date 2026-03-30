from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


db_url="postgresql://postgres:safwan123@localhost:5432/safwan"
engine=create_engine(db_url)

Session= sessionmaker(autocommit=False, autoflush=False,bind=engine)