from sqlalchemy import Column, Integer, String, Date, Time, Float, LargeBinary, DateTime, BigInteger, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from zoneinfo import ZoneInfo
from db.context import SubmssionsBase


class Submission(SubmssionsContext):
    __tablename__ = 'submissions'   
    
    submission_id = Column(BigInteger, primary_key=True, autoincrement=True, primary_key=True)
    file_name = Column(String(100), nullable=False)  
    upload_start_time = Column(DateTime, nullable=False)
    upload_end_time = Column(DateTime, nullable=True)
    file_path = Column(String(500), nullable=False) 
    processing_status_id = Column(Integer, ForeignKey('processing_status.processing_status_id'))
    processing_status = relationship('ProcessingStatus', back_populates='submissions')
    # Default MTN UTC
    load_date = Column(
        DateTime,
        default=lambda: datetime.now(datetime.UTC).astimezone(ZoneInfo("America/Denver"))
    )


class ProcessingStatus(SubmssionsContext):
    __tablename__ = 'processing_status'

    processing_status_id = Column(Integer, primary_key=True, autoincrement=True, primary_key=True)
    processing_status_description = Column(String(100), nullable=False)  
    submissions = relationship('Submission', back_populates='processing_status')
    # Default MTN UTC
    load_date = Column(
        DateTime,
        default=lambda: datetime.now(datetime.UTC).astimezone(ZoneInfo("America/Denver"))
    )
