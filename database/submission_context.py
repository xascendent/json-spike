import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SUBMISSION_DATABASE_URL = os.getenv("SUBMISSION_DATABASE_URL")
engine = create_engine(SUBMISSION_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)
StagingContext = declarative_base()


