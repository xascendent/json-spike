from sqlalchemy import text, bindparam
from database.context_deid import SessionLocal as deid_session
from database.context_staging import SessionLocal as staging_session
from database.models.deid import VisitsCheck, Narratives
from database.models.staging import Narratives as StagingNarratives

def pull_random_subset(submission_id):
    query = text("""        
        WITH cte AS (
            SELECT *, ROW_NUMBER() OVER (ORDER BY NEWID()) AS rn
            FROM [AIE5_Staging].[dbo].[visits]
            WHERE submission_id = :submission_id
        )
        SELECT *
        FROM cte
        WHERE rn <= CEILING((SELECT COUNT(*) * 0.05 FROM [AIE5_Staging].[dbo].[visits] WHERE submission_id = :submission_id))                 
    """)
    
    with staging_session() as session:
        # Use `mappings()` to return dictionary-like results
        result = session.execute(query, {"submission_id": submission_id}).mappings().all()
        data = result
    
    # Now you can reference by column name directly
    visit_ids = [row['visit_id_lnk'] for row in data if 'visit_id_lnk' in row]
    return data, visit_ids


def pull_narratives(visit_ids):
    try:
        if not visit_ids:
            return []
        
        query = text("""
            SELECT *
            FROM [AIE5_Staging].[dbo].[narratives]
            WHERE visit_id_lnk IN :visit_ids
        """).bindparams(bindparam("visit_ids", expanding=True))
        
        with staging_session() as session:
            result = session.execute(query, {"visit_ids": tuple(visit_ids)}).mappings().all()
        
        return result

    except Exception as e:
        print(f"Error during pull_narratives: {e}")



def visits_to_deid(visits_data):
    try:
        with deid_session() as session:  # Renamed to 'session'
            for row in visits_data:
                # Step 1: Insert visit into VisitsCheck
                visit = VisitsCheck(
                    visit_id_lnk=row['visit_id_lnk'],
                    site_name=row['site_name'],
                    submissionYYYYMM=row['submissionYYYYMM'],
                    submission_id=row['submission_id'],
                    ed_visit_id=row['ed_visit_id'],
                    ed_mrn=row['ed_mrn'],
                    review_batch_id=None,
                    human_reviewed=False,
                    llm_reviewed=False,
                    human_sensitive_found=False,
                    llm_sensitive_found=False,
                    load_date=row['load_date']
                )
                session.add(visit)            
            session.commit()
    except Exception as e:
        print(f"Error during visits_to_deid: {e}")
        # Create a new session to rollback since the original session is out of scope
        with deid_session() as session:
            session.rollback()

def narratives_to_deid(narratives_data):
    try:
        with deid_session() as session:  # Renamed to 'session'
            for row in narratives_data:            
                deid_narrative = Narratives(
                    visit_id_lnk=row['visit_id_lnk'],
                    site_name=row['site_name'],
                    submissionYYYYMM=row['submissionYYYYMM'],
                    narrative_text=row['narrative_text'],     
                    load_date=row['load_date']
                )
                session.add(deid_narrative)
            
            session.commit()            

    except Exception as e:
        print(f"Error during narratives_to_deid: {e}")
        # Create a new session to rollback since the original session is out of scope
        with deid_session() as session:
            session.rollback()

