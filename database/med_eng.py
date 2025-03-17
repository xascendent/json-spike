from database.context_grouping import SessionLocal as grouping_session
from database.context_staging import SessionLocal as staging_session
from database.models.grouping import Medications as GroupingMedications
from database.models.staging import Medications as StagingMedications
import json
from database.models.grouping import Medications


def pull_stg_hashed_medication_list(submission_id) -> list:
    with staging_session() as session:
        hashes = (
            session.query(
                StagingMedications.hash_medication_name,
                StagingMedications.medication_name
            )
            .filter(StagingMedications.submission_id == submission_id)
            .distinct()
            .all()
        )
    
    # Return a list of tuples: [(hash_medication_name, medication_name), ...]
    return [(row[0], row[1]) for row in hashes]


def get_grp_non_matched_hashed_medications(staging_data: list) -> list:
    if not staging_data:
        return []

    # Extract just the hashes from the data for the WHERE IN clause
    staging_hashes = [row[0] for row in staging_data]

    with grouping_session() as session:
        # Step 1: Pull matched hashes from the grouping table
        matched_hashes = (
            session.query(GroupingMedications.hash_medication_name)
            .filter(GroupingMedications.hash_medication_name.in_(staging_hashes))
            .distinct()
            .all()
        )
        
        # Step 2: Flatten the matched hashes into a set for fast lookup
        matched_hashes = {row[0] for row in matched_hashes}

        # Step 3: Find the non-matched hashes and their medication names
        non_matched = [
            (hash_val, med_name) for hash_val, med_name in staging_data 
            if hash_val not in matched_hashes
        ]
    
    return non_matched

def save_medication(hash_medication_name, medication_data):
    deserialized_medication = json.loads(medication_data)
    # Create a new Medications object
    medication = Medications(
        hash_medication_name=hash_medication_name,
        medication_name=deserialized_medication['medication_name'],
        opioid=deserialized_medication.get('opioid', False),
        antibiotic=deserialized_medication.get('antibiotic', False),
        nsaid=deserialized_medication.get('nsaid', False),
        rxnorm_mappings=json.dumps(deserialized_medication),  # Store the full JSON object as a string
        reviewed=False  # Default value
    )
    with grouping_session() as session:
        session.add(medication)
        session.commit()