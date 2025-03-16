from database.context_staging import SessionLocal
from sqlalchemy import text

def get_submission_info(submission_id):
    query = text("""
        SELECT site_name, submissionYYYYMM as submission_yyyymm
        FROM [dbo].[visits]
        WHERE submission_id = :submission_id
    """)

    with SessionLocal() as session:
        result = session.execute(query, {"submission_id": submission_id})
        site_name, submission_yyyymm = result.fetchone()

    return site_name, submission_yyyymm

def remove_failed_submission(submission_id):
    with SessionLocal() as session:
        # Use parameterized queries to prevent injection
        session.execute(
            text("DELETE FROM dbo.medications WHERE submission_id = :submission_id"),
            {"submission_id": submission_id}
        )
        session.execute(
            text("DELETE FROM dbo.narratives WHERE submission_id = :submission_id"),
            {"submission_id": submission_id}
        )
        session.execute(
            text("DELETE FROM dbo.visits WHERE submission_id = :submission_id"),
            {"submission_id": submission_id}
        )
        
        # Commit once after all statements
        session.commit()
        print(f"Submission {submission_id} removed from staging!")