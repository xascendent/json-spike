from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
from database.context_submission import SubmissionContext
from sqlalchemy.sql import func

class Submissions(SubmissionContext):
    __tablename__ = 'submissions'
    
    submission_id = Column(BigInteger, primary_key=True, autoincrement=True)
    file_name = Column(String(200), nullable=False)
    upload_start_time = Column(DateTime, nullable=False)
    upload_end_time = Column(DateTime, nullable=True)
    file_path = Column(String(500), nullable=False)
    
    # Foreign key reference to Statuses
    processing_status_id = Column(Integer, ForeignKey('statuses.processing_status_id'))
    
    # Auto load date from server time
    load_date = Column(DateTime, server_default=func.now())

    # Relationship back to Statuses
    processing_status = relationship('Statuses', back_populates='submissions')


class Statuses(SubmissionContext):
    __tablename__ = 'statuses'    
    processing_status_id = Column(Integer, primary_key=True)
    processing_status_description = Column(String(200), nullable=False)

    # Fix relationship name to match Submissions model
    submissions = relationship("Submissions", back_populates="processing_status")
