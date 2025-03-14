from database.staging_context import SessionLocal as staging_session
from database.submission_context import SessionLocal as submission_session
from sqlalchemy import text

def reset_demo_staging_sql():
    with staging_session() as session:
        # Execute multiple statements
        session.execute(text("DELETE dbo.medications"))
        session.execute(text("DELETE dbo.narratives"))
        session.execute(text("DELETE dbo.visits"))
        
        # Commit once after all statements
        session.commit()
        print("Demo system reset!")

        
def reset_demo_submission_sql():
    with submission_session() as session:
        # Execute multiple statements
        session.execute(text("DELETE dbo.submissions"))        
        
        # Commit once after all statements
        session.commit()
        print("Submission system reset!")