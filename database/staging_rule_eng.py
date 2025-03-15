from database.context_staging import SessionLocal
from sqlalchemy import text

def check_visits_for_dups(submission_id):
    query = text("""
        SELECT ed_visit_id, ed_mrn 
        FROM dbo.visits 
        WHERE submission_id = :submission_id
        GROUP BY ed_visit_id, ed_mrn
        HAVING COUNT(*) > 1
    """)

    with SessionLocal() as session:
        result = session.execute(query, {"submission_id": submission_id})
        duplicates = result.fetchall()
        
    return duplicates
