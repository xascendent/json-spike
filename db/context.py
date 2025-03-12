import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SUBMISSIONSSTAGINGDB_URL = os.getenv("SUBMISSIONSSTAGINGDB_URL")
engine = create_engine(SUBMISSIONSSTAGINGDB_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)
SubmssionsContext = declarative_base()
