import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

WAREHOUSE_DATABASE_URL = os.getenv("WAREHOUSE_DATABASE_URL")
engine = create_engine(WAREHOUSE_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)
WarehouseContext = declarative_base()