from sqlalchemy import Column, String, Integer, BigInteger, DateTime, ForeignKey, Boolean, LargeBinary, Date, Time, Text
from database.context_grouping import GroupingContext

class Medications(GroupingContext):
    __tablename__ = 'medications_group'    
    medication_id = Column(BigInteger, primary_key=True, autoincrement=True)
    hash_medication_name = Column(LargeBinary(32), nullable=False)
    medication_name = Column(Text, nullable=False)
    opioid = Column(Boolean, nullable=False)
    antibiotic = Column(Boolean, nullable=False)
    nsaid = Column(Boolean, nullable=False)
    rxnorm_mappings = Column(Text, nullable=True)
    reviewed = Column(Boolean, nullable=False)