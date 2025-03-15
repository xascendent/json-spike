from sqlalchemy import Column, Integer, String, Date, Time, LargeBinary, ForeignKey, Text, BigInteger, DateTime
from database.context_warehouse import WarehouseContext
from sqlalchemy.orm import relationship

class Visits(WarehouseContext):
    __tablename__ = 'visits'
    
    # Binary fields for SHA256 identifiers
    visit_id_lnk = Column(LargeBinary(32), primary_key=True)
    # Submission details
    site_name = Column(String(100), nullable=False)  
    submissionYYYYMM = Column(Integer, nullable=False)     
    submission_id = Column(BigInteger, nullable=True)

    ed_visit_id = Column(LargeBinary(32), nullable=False)
    ed_mrn = Column(LargeBinary(32), nullable=False)
    

    # Identity fields
    birth_date = Column(Date, nullable=False) 
    sex = Column(String(10), nullable=False)  
    ed_door_date = Column(Date, nullable=False) 
    ed_door_time = Column(Time, nullable=False)
    load_date = Column(DateTime, nullable=False)

    # Relationships
    medications = relationship("Medications", back_populates="visit", cascade="all, delete-orphan")
    narratives = relationship("Narratives", back_populates="visit", cascade="all, delete-orphan")
    

class Medications(WarehouseContext):
    __tablename__ = 'medications'    
    medication_id = Column(BigInteger, primary_key=True, autoincrement=True) # since we can release just the staging we will leave this as autoincrement and not push from the stg
    visit_id_lnk = Column(LargeBinary(32), ForeignKey('visits.visit_id_lnk'))
    site_name = Column(String(100), nullable=False)
    submissionYYYYMM = Column(Integer, nullable=False)
    submission_id = Column(BigInteger, nullable=True)
    hash_medication_name = Column(LargeBinary(32), nullable=False)
    medication_name = Column(Text, nullable=False)
    order_entry_date = Column(Date, nullable=False)
    order_entry_time = Column(Time, nullable=False)
    medication_route = Column(Text, nullable=False)
    load_date = Column(DateTime, nullable=False)

    # Relationship back to Visits
    visit = relationship("Visits", back_populates="medications")


class Narratives(WarehouseContext):
    __tablename__ = 'narratives'    
    narrative_id = Column(BigInteger, primary_key=True, autoincrement=True)
    visit_id_lnk = Column(LargeBinary(32), ForeignKey('visits.visit_id_lnk'))
    site_name = Column(String(100), nullable=False)
    submissionYYYYMM = Column(Integer, nullable=False)
    submission_id = Column(BigInteger, nullable=True)
    
    narrative_text = Column(Text, nullable=False)
    narrative_author = Column(String(200), nullable=False)
    narrative_type = Column(String(200), nullable=False)
    load_date = Column(DateTime, nullable=False)

    # Relationship back to Visits
    visit = relationship("Visits", back_populates="narratives")