import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DEID_DATABASE_URL = os.getenv("DEID_DATABASE_URL")
engine = create_engine(DEID_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)
DeidContext = declarative_base()


