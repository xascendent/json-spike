from sqlalchemy import Column, Integer, String, Date, Time, Float, LargeBinary, DateTime
from datetime import datetime
from zoneinfo import ZoneInfo
from db.context import SubmssionsBase


class Submissions(SubmssionsBase):
    __tablename__ = 'submissions'
    
    # Binary fields for SHA256 identifiers
    patient_identifier = Column(LargeBinary(32), primary_key=True)
    ed_mrn = Column(LargeBinary(32), nullable=False)
    visit_id = Column(LargeBinary(32), nullable=False)

    # Submission details
    submission_yyyymm = Column(Integer, nullable=False) 
    site = Column(String(100), nullable=False)  
    schema_version = Column(Float, nullable=False)  
    
    # Identity fields
    birth_date = Column(Date, nullable=False) 
    sex = Column(String(50), nullable=False)  
    ed_door_date = Column(Date, nullable=False) 
    ed_door_time = Column(Time, nullable=False) 
    
    # Default MTN UTC
    load_date = Column(
        DateTime,
        default=lambda: datetime.now(datetime.UTC).astimezone(ZoneInfo("America/Denver"))
    )