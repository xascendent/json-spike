from sqlalchemy import Column, String, Integer, BigInteger, DateTime, ForeignKey, Boolean, LargeBinary
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.context_submission import SubmissionContext

class VisitsCheck(SubmissionContext):
    __tablename__ = 'visits_check'
    
    visit_id_lnk = Column(LargeBinary(32), primary_key=True)
    site_name = Column(String(100), nullable=False)
    submissionYYYYMM = Column(Integer, nullable=False)
    submission_id = Column(BigInteger, nullable=True)
    ed_visit_id = Column(LargeBinary(32), nullable=False)
    ed_mrn = Column(LargeBinary(32), nullable=False)
    review_batch_id = Column(LargeBinary(32), nullable=True)
    human_reviewed = Column(Boolean, server_default='0')
    llm_reviewed = Column(Boolean, server_default='0')
    human_sensitive_found = Column(Boolean, server_default='0')
    llm_sensitive_found = Column(Boolean, server_default='0')
    load_date = Column(DateTime(timezone=True), server_default=func.sysdatetimeoffset())

    # Relationship to narratives
    narratives = relationship("Narratives", back_populates="visit")


class Narratives(SubmissionContext):
    __tablename__ = 'narratives'
    
    visit_id_lnk = Column(LargeBinary(32), ForeignKey('visits_check.visit_id_lnk'), primary_key=True)
    site_name = Column(String(100), nullable=False)
    submissionYYYYMM = Column(Integer, nullable=False)
    narrative_text = Column(String, nullable=False)
    load_date = Column(DateTime(timezone=True), server_default=func.sysdatetimeoffset())

    # Back reference to VisitsCheck
    visit = relationship("VisitsCheck", back_populates="narratives")
